import sqlite3


class DataBase:
    def __init__(self, name):
        self.name = name
        self.conn = sqlite3.connect(self.name)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users(user, schoolID, answers, correctAnswersPercentage)"
        )
        self.conn.commit()

    def add_data(self, user, school_ID, answers, correct_AP):
        self.user = user
        self.school_ID = school_ID
        self.answers = answers
        self.correctAP = correct_AP
        self.cur.execute(
            "INSERT INTO users (user, schoolID, answers, correctAnswersPercentage) VALUES ('%s', '%s', '%s', '%s')"
            % (user, school_ID, answers, correct_AP)
        )
        self.conn.commit()

    def count(self):
        self.cur.execute("SELECT COUNT(*) FROM users")
        total_users = self.cur.fetchone()[0]
        self.cur.close()
        self.conn.close()
        return total_users

    def select(self):
        self.cur.execute("SELECT*FROM users")
        users = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        return users

    def delete_all(self):
        self.cur.execute("DELETE FROM users")
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def select_first(self):
        self.cur.execute("SELECT*FROM users")
        user_data = self.cur.fetchone()
        self.cur.close()
        self.conn.close()
        return user_data

    def select_last(self):
        self.cur.execute("SELECT*FROM users ORDER BY rowid DESC LIMIT 1")
        user_data = self.cur.fetchone()
        self.cur.close()
        self.conn.close()
        return user_data

    def update(self, schoolID, correctAP):
        self.correctAP = correctAP
        self.schoolID = schoolID
        self.cur.execute(
            "UPDATE users SET correctAnswersPercentage = ? WHERE schoolID = ?",
            (self.correctAP, self.schoolID),
        )
        self.conn.commit()
        self.cur.close()
        self.conn.close()
