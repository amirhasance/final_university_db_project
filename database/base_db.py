import mysql.connector
from datetime import datetime


class BaseDatabase():
    database_url = "127.0.0.1"
    database_user = "root"
    database_password = "root"
    database_name = "project"

    def __init__(self):
        self.db_conn = self.get_db_connection()
        self.cursor = self.get_cursor()
        self.create_tables()

    def get_db_connection(self, db_name=None):
        if not db_name:
            db_name = self.database_name
        conn = mysql.connector.connect(
            host=self.database_url,
            user=self.database_user,
            password=self.database_password,
            database=db_name
        )
        return conn

    def get_cursor(self):
        return self.db_conn.cursor()

    def create_tables(self):
        mydb = mysql.connector.connect(
            host=self.database_url,
            user=self.database_user,
            password=self.database_password,

        )
        myCursor = mydb.cursor()
        myCursor.execute("SHOW DATABASES")

        databases = []

        for db in myCursor:
            databases.append(db[0])
        # If database doesn't exist it will create it
        if not databases.__contains__('project'):
            myCursor.execute("CREATE DATABASE DBProj")
            print("database created")

        mydb.close()

        # Create tables and insert data into them
        myCursor = self.cursor
        self.cursor.execute("SHOW TABLES")
        tables = []

        for db in myCursor:
            tables.append(db[0])

        if not tables.__contains__('user'):
            myCursor.execute("""
                            create table user
                (
                    first_name          varchar(255) not null,
                    last_name           varchar(255) not null,
                    phone               varchar(25)  not null,
                    email               varchar(254) not null,
                    username            varchar(255) not null
                        primary key,
                    password            varchar(255) not null,
                    security_question   varchar(255) null,
                    sec_question_answer varchar(255) not null,
                    is_logged_in        tinyint(1)   not null,
                    constraint phone
                        unique (phone)
                );
""")
            print("users created")
        if not tables.__contains__('message'):
            myCursor.execute("""
                create table message
                (
                    id       bigint auto_increment
                        primary key,
                    text     longtext   null,
                    is_seen  tinyint(1) not null,
                    is_liked tinyint(1) not null
                );""")

        if not tables.__contains__('sending'):
            myCursor.execute("""
                create table sending
                (
                    id           bigint auto_increment
                        primary key,
                    msg_datetime datetime(6)  not null,
                    message_id   bigint       not null,
                    sender_id    varchar(255) not null,
                    constraint myapp_sending_message_id_9ae0aeb6_fk_myapp_message_id
                        foreign key (message_id) references message (id),
                    constraint myapp_sending_sender_id_3c6bbe78_fk_myapp_user_username
                        foreign key (sender_id) references user (username)
                );""")
        if not tables.__contains__('receiving'):
            myCursor.execute("""
                create table receiving
                (
                    id           bigint auto_increment
                        primary key,
                    msg_datetime datetime(6)  not null,
                    message_id   bigint       not null,
                    receiver_id  varchar(255) not null,
                    constraint myapp_receiving_message_id_249a2523_fk_myapp_message_id
                        foreign key (message_id) references message (id),
                    constraint myapp_receiving_receiver_id_bf58c659_fk_myapp_user_username
                        foreign key (receiver_id) references user (username)
                );""")

        if not tables.__contains__('log'):
            myCursor.execute("""
                create table log
                (
                    id      bigint auto_increment
                        primary key,
                    message longtext    not null,
                    time    datetime(6) not null
                );""")
        if not tables.__contains__('friendship'):
            myCursor.execute("""
                create table friendship
                (
                    id           bigint auto_increment
                        primary key,
                    from_user_id varchar(255) not null,
                    to_user_id   varchar(255) not null,
                    constraint myapp_frindship_from_user_id_to_user_id_41c04bdf_uniq
                        unique (from_user_id, to_user_id),
                    constraint myapp_frindship_from_user_id_1e4b1838_fk_myapp_user_username
                        foreign key (from_user_id) references user (username),
                    constraint myapp_frindship_to_user_id_95dd3fde_fk_myapp_user_username
                        foreign key (to_user_id) references user (username)
                );

            """)

        if not tables.__contains__('friendship_request'):
            myCursor.execute("""
                create table friendship_request
                (
                    id           bigint auto_increment
                        primary key,
                    time         datetime(6)  not null,
                    from_user_id varchar(255) not null,
                    to_user_id   varchar(255) not null,
                    constraint myapp_friendshiprequest_from_user_id_to_user_id_ff3e66d4_uniq
                        unique (from_user_id, to_user_id),
                    constraint myapp_friendshiprequ_from_user_id_b62a07d0_fk_myapp_use
                        foreign key (from_user_id) references user (username),
                    constraint myapp_friendshiprequ_to_user_id_f63b406a_fk_myapp_use
                        foreign key (to_user_id) references user (username)
                );""")

        if not tables.__contains__('block'):
            myCursor.execute("""
                create table block
                (
                    id                bigint auto_increment
                        primary key,
                    blocking_datetime datetime(6)  not null,
                    from_user_id      varchar(255) not null,
                    to_user_id        varchar(255) not null,
                    constraint myapp_block_from_user_id_to_user_id_af51f0b9_uniq
                        unique (from_user_id, to_user_id),
                    constraint myapp_block_from_user_id_270a7c44_fk_myapp_user_username
                        foreign key (from_user_id) references user (username),
                    constraint myapp_block_to_user_id_8c7ed49d_fk_myapp_user_username
                        foreign key (to_user_id) references user (username)
                );""")
