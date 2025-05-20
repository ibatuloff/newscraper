import psycopg2
from scrapy.exceptions import DropItem
from newscraper import settings
from newscraper.logger import logger



class DuplicateFilterPipeline:

    def process_item(self, item, spider):
        self.cur.execute(
            """
            SELECT 1
            FROM publication
            WHERE url = %s;
            """, item.get('url')
        )
        if self.cur.fetchone():
            # если такая статья уже есть в базе, то выкидываем её
            logger.info(f"Статья {item.get('url')} уже есть в базе. Пропускаем.")
            raise DropItem(f"Статья {item.get('url')} уже есть в базе.")
        # если такой статьи в базе нет, то отправляем дальше по конвееру
        return item




class DatabasePipeline:

    @classmethod
    def from_crawler(cls, crawler):
        pipe = cls()
 
        pipe.conn_data = {
            'host': crawler.settings.get('HOST1'),
            'port': crawler.settings.get('DB_PORT'),
            'dbname': crawler.settings.get('DB_NAME'),
            'user': crawler.settings.get('DB_USER'),
            'password': crawler.settings.get('DB_PASSWORD'),
            'sslmode': 'verify-full',
            'sslrootcert': crawler.settings.get('CA_PATH')
        }
        return pipe
    def open_spider(self, spider):
        self.conn = psycopg2.connect(**self.conn_data)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        upsert_sql = """
            INSERT INTO site (name, url)
            VALUES (%s, %s)
            ON CONFLICT (url) DO UPDATE SET name = EXCLUDED.name
            RETURNING id;
        """

        insert_sql = """
            INSERT INTO publication (title, text, url, site_id, published_at)
            VALUES (%s, %s, %s, %s, %s);
        """

        self.cur.execute(upsert_sql, (
            spider.site_name, spider.site_url
        ))
        site_id = self.cur.fetchone()[0]

        self.cur.execute(insert_sql, (
            item.get('title'),
            item.get('content'),
            item.get('url'),
            site_id,
            int(item.get('date').timestamp()) * 1000 # конвертация в миллисекунды
        ))

        self.conn.commit()
        return item