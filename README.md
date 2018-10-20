#### WARNING: This is not a secure setup of a server.  It will be hackable on the public internet.  Brute force attacks will succeed on this server.  Do not put anything on this PC that you don't want known by others!!  Also, it is possible if this server were compromised it could be used to launch attacks on other computers in your home network.  You are allowing public connections to a computer on your network and that's inherently risky.

1. Setup SSH hosting.
* In your server

2. Setup a private static IP.
* In your router
* Login to your router and take not of the current dynamic IP address assigned to your server.
* Use router features to assign that IP as a static IP.  This IP is only relevant to your private network.

2. You need a Dynamic DNS client.
* In your router or server.  Prefering router.
* Because your public IP changes periodically (enforced by your ISP) you will need to update a public DNS service so that you continue to be discoverable by public clients (like me).
* Choose to use either a firmware feature in your router or to do this with Linux software on the server itself.
* If you choose to use the router then make note of which Dynamic DNS services it can support.

3. Setup an account with a free Dynamic DNS service.  Your router will constrain your choices here or you can choose any of them if you chose to use Linux client software instead.  I'm going to assume your router supports the "no-IP" provider and you've chosen to use it.
* Setup an account at https://www.noip.com/.
* Login to your router and enter your account information and the DNS name you created with your account:  nis-food.ddns.net
* [no-IP Instructional Video -- Router Setup with DNS name](https://www.youtube.com/watch?v=EH8wJt81bqg)

4. Setup port forwarding.
* In your router
* Each network service you host on your server will have a TCP port number.  Like SSH=22, PostgreSQL=5432, etc.
* You want to expose those ports publically on the internet.  You're setting up your router as a passthrough so those TCP connections are made between public clients and your private server.  The router will be a TCP bridge.
* [no-IP Instructional Video -- Port Forwarding](https://www.youtube.com/watch?v=CLunOJZqmc0)
