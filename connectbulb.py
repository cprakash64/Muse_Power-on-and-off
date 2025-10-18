from phue import Bridge

# Connect to the bridge
b = Bridge('your_bridge_ip_address')

# Turn on the light
b.set_light('Your Light Name', 'on', True)
