package main

import (
	"flag"
	"fmt"
	"os"
	"syscall"
)

type file struct {
	fd   syscall.Handle // file descriptor number
	name string         // file name
}

var (
	stdin  = newFile(0, "/dev/stdin")
	stdout = newFile(1, "/dev/stdout")
	stderr = newFile(2, "/dev/stderr")
)

func (f *file) close() (err error) {
	if f == nil {
		return syscall.EINVAL
	}
	e := syscall.Close(f.fd)
	f.fd = syscall.InvalidHandle
	if e != nil {
		return e
	}

	return nil
}

func (f *file) read(content []byte) (ret int, err error) {
	if f == nil {
		return -1, syscall.EINVAL
	}

	ret, e := syscall.Read(f.fd, content)
	if e != nil {
		err = e
	}
	return ret, err
}

func (f *file) write(content []byte) (ret int, err error) {
	if f == nil {
		return -1, syscall.EINVAL
	}

	ret, e := syscall.Write(f.fd, content)
	if e != nil {
		err = e
	}
	return ret, err
}

func newFile(fd syscall.Handle, name string) *file {
	if fd == syscall.InvalidHandle {
		return nil
	}
	return &file{fd, name}
}

func open(name string, mode int, perm uint32) (f *file, err error) {
	r, e := syscall.Open(name, mode, perm)
	if e != nil {
		err = e
	}
	return newFile(r, name), err
}

// func cat(f *file) {

// }

func main() {
	flag.Parse()
	fmt.Println("test")
	if flag.NArg() != 0 {
		os.Exit(1)
	}

	output := []byte("Hello world\n")
	fmt.Printf("Output: %s", output)
	stdout.write(output[:])

	var content []byte
	f, err := open(`D:\download\config.toml`, 0, 0)
	if f == nil {
		fmt.Printf("Can not open file; err=%s\n", err)
	}

	ret, err := f.read(content[:])
	if ret > 0 {
		fmt.Printf("Open file: %s", content)
	} else {
		fmt.Printf("Error info: %s", err)
	}
}
