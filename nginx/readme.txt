#setup step
sudo apt-get install nginx

#link /etc/nginx/nginx.conf to your CWD to easy modify config  
#before link ,please rm exist nginx.conf first
ln -s /your-application-path/nginx.conf  nginx.conf

#setting your config
please check nginx_setup.pdf for more info

#check config seeting is ok
sudo nginx -t

---you can go to next step when you using nginx -t and see message below 
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

#regular cmd (start nginx, check nginx state , stop nginx)
sudo service nginx start
sudo service nginx status
sudo service nginx stop

#run game with nginx
sudo service nginx start
python web.py -port=8888 -game=2

