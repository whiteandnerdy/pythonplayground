1. You need a Dynamic DNS client.  As your public IP changes periodically (enforced by your ISP) you will need to update a public DNS service so you're still resolveable by public clients (like me).
* Choose to use either a firmware feature in your router or to do this with Linux software on the server itself.
* If you choose to use the router then make note of which Dynamic DNS services it can support.

2. Setup an account with a free Dynamic DNS service.  Your router will constrain your choices here or you can choose any of them if you chose to use Linux client software instead.  I'm going to assume your router supports the "no-IP" provider and you've chosen to use it.
* Setup an account at https://www.noip.com/.
* Login to your router and enter your account information and the DNS name you created with your account:  nis-food.ddns.net
* [no-IP Instructional Video -- Router Setup with DNS name](https://www.youtube.com/watch?v=EH8wJt81bqg)

3. Setup port forwarding.
* [no-IP Instructional Video -- Port Forwarding](https://www.youtube.com/watch?v=CLunOJZqmc0)
