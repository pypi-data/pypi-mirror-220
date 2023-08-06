import logging
from time import sleep

from test_bed_adapter import TestBedOptions, TestBedAdapter
from test_bed_adapter.kafka.consumer_manager import ConsumerManager

logging.basicConfig(level=logging.INFO)

tb_options = {
    "consumer_group": 'url_checker',
    "kafka_host": '127.0.0.1:3501',
    "schema_registry": 'http://127.0.0.1:3502',
    "message_max_bytes": 1000000,
    "partitioner": 'random',
    "offset_type": 'earliest',
}

TESTBED_OPTIONS = TestBedOptions(tb_options)
test_bed_adapter = TestBedAdapter(TESTBED_OPTIONS)

f = open('urls.txt', 'w')
counter = 0
urls = []


def handle_message(message, topic):
    # print(message['url'])
    global counter
    counter += 1
    urls.append(message['url'] + '\t' + message['id'])
    if counter % 1000 == 0:
        print(counter)
        f.write("\n".join(urls))
        urls.clear()
        f'{message["url"]}\t{message["id"]}\n'


# test_bed_adapter.initialize()
ConsumerManager(options=TESTBED_OPTIONS, kafka_topic='article_raw_ru', handle_message=handle_message).start()
sleep(1000)
f.close()

# try:
# wait for some time
# finally:
# Stop test bed
# test_bed_adapter.stop()

# print(len(urls))
# write to file
# for url, messages in urls.items():
#     f.write(f'{url}\t{len(messages)}\n')
