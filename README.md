# DNS 

In this project we created a program that changes the operating system's default **systemd-resolved** to our DNS implementation.



It's just to modifying the file`/etc/resolv.conf` .

In modern Linux systems `/etc/resolv.conf` often points to 127.0.0.53, and this is a simbolic link 

```bash
ls -l /etc/resolv.conf
lrwxrwxrwx 1 root root 39 Feb 27 10:00 /etc/resolv.conf -> ../run/systemd/resolve/stub-resolv.conf

```

Here *l* in *lrwxrwxrwx* indicates a symbolic link.

How to configure our DNS.

1. Deactivate a systemd-resolved :
   ```bash	
   sudo systemctl stop systemd-resolved
   sudo systemctl disable systemd-resolved
   ```

2. To configure the `etc/resolve.conf` file, replace the symbolic link with a static file.

   ```bash
   sudo rm /etc/resolv.conf
   sudo nano /etc/resolv.conf
   ```

3. Configure the address and the port of our program.

   1. Changue the parameters in main.cpp, in this case is localhost and the port is 53 for standard DNS queries.

      ```cpp
      #main.cpp
      int main() {
          DnsServer server("127.0.0.1", 53);
          server.start();
          return 0;
      }
      ```

   2. Execute the program

4. Configure the `etc/resolve.conf` 

   ```bash
   # This is /run/systemd/resolve/stub-resolv.conf managed by man:systemd-resolved(8).
   # Do not edit.
   # ..........
   
   #nameserver 127.0.0.53
   nameserver 127.0.0.1 #To send dns query to our dns server
   options edns0 trust-ad
   search .
   
   ```

   

