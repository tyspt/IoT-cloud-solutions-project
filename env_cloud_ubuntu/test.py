import global_config as config

topic = config.TOPIC_PREFIX_SENSOR + "pressure/psi"

sub_topic = topic.split(config.TOPIC_PREFIX_SENSOR)[1]
print(sub_topic.split('/'))

sub_topic, unit = sub_topic.split('/')

print(sub_topic)
print(unit)