// forgepanel-host-observe is a nonprivileged host inventory tool.
// No arguments, shell, DNS query, TLS dial, or system mutation is supported.
package main

import (
    "encoding/json"
    "fmt"
    "os"

    "github.com/yyogas/forgepanel/tools/host-address-observation/observer"
)

func main() {
    if len(os.Args)!=1 {
        fmt.Fprintln(os.Stderr,"usage: forgepanel-host-observe (no arguments)")
        os.Exit(2)
    }
    encoder:=json.NewEncoder(os.Stdout)
    encoder.SetIndent("","  ")
    if err:=encoder.Encode(observer.InspectHost()); err!=nil {
        fmt.Fprintln(os.Stderr,"failed to encode read-only host observation")
        os.Exit(1)
    }
}
