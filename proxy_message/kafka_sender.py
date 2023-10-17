# https://www.red-gate.com/simple-talk/development/dotnet-development/setting-up-a-kafka-test-environment-with-kafdrop/
import json
from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
from kafka.errors import KafkaError
from loguru import logger
import pytz

from config import settings
from proxy_message.utils import combine_hash


def create_topics(topic):
    client = KafkaAdminClient(bootstrap_servers=settings.kafka_host)
    if topic in client.list_topics():
        return ''
    else:
        topic_list = [NewTopic(name=topic, num_partitions=settings.partition_count, replication_factor=1)]
        client.create_topics(new_topics=topic_list, validate_only=False)


def get_producer():
    return KafkaProducer(
            bootstrap_servers=settings.kafka_host,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            retries=10,
        )


def send_cases_to_kafka(message):
    text_message = message.text
    date_message = message.date.astimezone(pytz.timezone('Europe/Moscow'))

    create_topics(settings.topic)
    try:
        producer = get_producer()
    except KafkaError as e:
        logger.exception(f'Failed to initiated KafkaProducers: {e}')
        raise e

    message = {
        'key_hash': combine_hash(text_message),
        'text_message': text_message,
        'date_message': str(date_message)
        # 'case_uid': str(case.case_uid),
        # 'case_number': case.case_number,
        # 'registration_date': str(case.registration_date.date()) if case.registration_date else None,
        # 'case_category': case.case_category,
        # 'case_code': case.case_code,
        # 'claim_sum': str(case.claim_sum),
        # 'close_date': str(case.close_date.date()) if case.close_date else None,
        # 'court_name': case.court_name,
        # 'is_simple_justice': case.is_simple_justice,
        # 'result_code': case.result_code,
        # 'is_approved': case.is_approved,
        # 'is_active': case.is_active,
        # 'court_tag': case.court_tag,
        # 'hash': str(case.hash),
    }
    producer.flush()

    try:
        producer.send(topic=settings.topic, key=str(combine_hash(text_message)).encode(), value=message).get(timeout=10)

    except KafkaError as e:
        logger.exception(f'MESSAGE send to Kafka  failed: {e}')
        raise e
