#!/bin/sh
# Start rsyslog
rsyslogd

# Get container name
CONTAINER_NAME=$(hostname)
# Update Zabbix agent config with the hostname
sed -i "s/Hostname=.*/Hostname=$CONTAINER_NAME/" /etc/zabbix/zabbix_agent2.conf
#Start Zabbix Agent 2
/usr/sbin/zabbix_agent2 &

# Start your app
exec python main.py >> /var/log/out.log 2>> /var/log/error.log