package main

import (
	"fmt"
	"io/ioutil"
	"net"
	"os/exec"
	"sort"
	"strconv"
	"strings"
	"time"
)

const tcpRetrans string = "netstat -s | awk '{if($2==\"segments\")a[$2$3$4]=$1}END{print a[\"segmentsretransmited\"]\"++\"a[\"segmentssendout\"]}'"

type flowData struct {
	total float64
	avg   float64
	max   float64
}

type ipInfo struct {
	ip        net.IP
	isPublic  bool
}

var excludeName = []string {"lo", "ppy", "docker", "mgt", "br-"}

func isPublicIP(ip net.IP) bool {
	if ip != nil {
		if (ip[0] == 192) && (ip[1] == 168) {
			return false
		} else if ip[0] == 10 {
			return false
		} else if ip[0] == 100 {
			return false
		} else if (ip[0] == 172) && (ip[1] >= 16) && (ip[1] < 32){
			return false
		} else {
			return true
		}
	}
	return false
}

func getLocalIPs() (map[string] ipInfo, error) {
	local := make(map[string] ipInfo)

	ift, err := net.Interfaces()
	if err != nil {
		return nil, err
	} else {
		fmt.Printf("Device ifaces: %v\n", ift)
	}

	outLoop:
		for _, item := range ift {
			for _, s := range excludeName {
				if strings.Contains(item.Name, s) {
					fmt.Printf("Interface name: %s, exclude\n", item.Name)
					continue outLoop
				}
			}

			addrs, err := item.Addrs()
			if err != nil {
				fmt.Printf("Can not get interface addrs: %v\n", err)
				continue
			} else {
				fmt.Printf("Name: %s, addrs: %v\n", item.Name, addrs)
			}
			for _, it := range addrs {
				var ip net.IP
				switch it := it.(type) {
				case *net.IPNet:
					ip = it.IP.To4()
				case *net.IPAddr:
					ip = it.IP.To4()
				}
				if ip != nil && ip.IsGlobalUnicast() {
					fmt.Printf("Name: %s, ipv4: %v\n", item.Name, ip)
					local[item.Name] = ipInfo{ip, isPublicIP(ip)}
				}
			}
		}
	fmt.Printf("local ips: %v\n", local)
	return local, nil
}

func filterDialInterface(allIf map[string] ipInfo) map[string] ipInfo {
	dialInterface := map[string] ipInfo{}
	for key, item := range allIf {
		if item.isPublic {
			dialInterface[key] = item
		}
	}

	if len(dialInterface) == 0 {
		for key, item := range allIf {
			if strings.Contains(strings.ToLower(key), "wan") {
				dialInterface[key] = item
			}
		}
	}

	if len(dialInterface) == 0 {
		dialInterface = allIf
	}
	return dialInterface
}

// get machine local ifconfig
func getIfconfig() ([]string, map[string] ipInfo) {
	ips, err := getLocalIPs()
	if err != nil {
		fmt.Printf("get local IPs error: %v\n", err)
		return []string{}, map[string] ipInfo{}
	}

	tmp := filterDialInterface(ips)
	var netCardName []string
	for key := range tmp {
		netCardName = append(netCardName, key)
	}
	return netCardName, tmp
}

func calculateFlow(card string) float64 {
	var flowValue float64 = 0
	path := fmt.Sprintf("/sys/class/net/%s/statistics/tx_bytes", card)
	content, err := ioutil.ReadFile(path)
	if err != nil {
		fmt.Printf("Can not read file %s, reason: %v\n", path, err)
		return flowValue
	}

	tmp := strings.Replace(string(content[:]), "\n", "", -1)
	flowValue, err = strconv.ParseFloat(tmp, 64)
	if err != nil {
		fmt.Printf("File %s content parse to float error: %v\n", path, err)
		return flowValue
	}
	return flowValue
}

func getCurrentFlow(duration time.Duration, netCard string, ch chan flowData){
	var totalFlow float64 = 0
	var avgFlow float64 = 0
	var maxFlow float64 = 0
	dataStorage := make([]float64, 0)
	stopTicker := time.NewTicker(time.Second * duration)
	defer stopTicker.Stop()

	currentFlow := calculateFlow(netCard)

	secondTicker := time.NewTicker(time.Second * 1)
	defer secondTicker.Stop()
	OuterLoop:
		for {
			select {
			case <-stopTicker.C:   // 停止流量统计
				break OuterLoop
			case <-secondTicker.C: // 统计每秒钟流量
				tmpFlow := calculateFlow(netCard)
				if currentFlow < tmpFlow {
					dataStorage = append(dataStorage, tmpFlow - currentFlow)
					currentFlow = tmpFlow
				}
			}
		}

	sort.Float64s(dataStorage)
	for _, v := range dataStorage {
		totalFlow += v
	}
	totalFlow = totalFlow * 8
	if len(dataStorage) > 0 {
		avgFlow = totalFlow / float64(len(dataStorage))
	}
	if len(dataStorage) > 0 {
		maxFlow = dataStorage[len(dataStorage) - 1] * 8
	}
	result := flowData{totalFlow, avgFlow, maxFlow}
	ch <- result
}

func asyncStatisticFlow(duration time.Duration, netCards []string, ch chan map[string] flowData) {
	result := make(map[string] flowData)
	dataChs := make(map[string] chan flowData, len(netCards))
	for _, card := range netCards {
		dataChs[card] = make(chan flowData, 1)
		go getCurrentFlow(duration, card, dataChs[card])
	}
	for name, oneCh := range dataChs{
		data, ok := <-oneCh
		if ok == false {
			fmt.Printf("Channel[%s] closed\n", name)
		} else {
			result[name] = data
			fmt.Printf("net card: %v, avg flow: %v\n", name, data.avg)
		}
	}
	ch <- result
}

func getTCPRetransmission() (int64, int64) {
	result, err := ExecResult(tcpRetrans)
	if err != nil {
		fmt.Printf("Fetch TCP retransmission error %v\n", err)
		return 0, 0
	}

	arr := strings.Split(result, "++")
	if len(arr)  < 2 {
		fmt.Printf("Fetch TCP retransmission result error %v\n", arr)
		return 0, 0
	}

	resend, _ := strconv.ParseInt(arr[0], 10, 64)
	send, _ := strconv.ParseInt(arr[1], 10, 64)
	return resend, send
}

func ExecResult(cmd string) (string, error) {
	out, err := exec.Command("bash", "-c", cmd).Output()
	if err != nil {
		fmt.Printf("Failed to execute command: %v", cmd)
		return "", err
	}

	outStr := strings.Trim(string(out), "\n")
	fmt.Printf(" result: %v", outStr)
	return outStr, nil
}

func main() {
	netCards, _ := getIfconfig()
	fmt.Printf("net cards: %v\n", netCards)
	ch := make(chan map[string] flowData)
	go asyncStatisticFlow(60, netCards, ch)
	result := <- ch
	var total float64 = 0
	for _, v := range result {
		total += v.avg
	}
	fmt.Printf("Flow result: %v mb\n", total / 1024 / 1024)
}
