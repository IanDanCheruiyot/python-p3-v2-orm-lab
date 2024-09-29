from __init__ import CURSOR, CONN
from department import Department
from employee import Employee

class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            summary TEXT NOT NULL,
            employee_id INTEGER NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row or update an existing row. """
        if self.id is None:
            # Insert a new row
            sql = """
                INSERT INTO reviews (year, summary, employee_id)
                VALUES (?, ?, ?)
            """
            CURSOR.execute(sql, (self.year, self.summary, self.employee_id))
            self.id = CURSOR.lastrowid
            Review.all[self.id] = self
        else:
            # Update an existing row
            sql = """
                UPDATE reviews
                SET year = ?, summary = ?, employee_id = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.year, self.summary, self.employee_id, self.id))
        CONN.commit()

    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        review = cls(year, summary, employee_id)
        review.save()
        return review

    @classmethod
    def instance_from_db(cls, row):
        """ Return a Review instance having the attribute values from the table row. """
        review_id, year, summary, employee_id = row
        if review_id in cls.all:
            return cls.all[review_id]
        else:
            review = cls(year, summary, employee_id, review_id)
            cls.all[review_id] = review
            return review

    @classmethod
    def find_by_id(cls, id):
        """ Return a Review instance having the attribute values from the table row. """
        if id in cls.all:
            return cls.all[id]
        else:
            sql = "SELECT * FROM reviews WHERE id = ?"
            CURSOR.execute(sql, (id,))
            row = CURSOR.fetchone()
            if row:
                return cls.instance_from_db(row)
            return None

    def update(self):
        """ Update the table row corresponding to the current Review instance. """
        if self.id:
            sql = """
                UPDATE reviews
                SET year = ?, summary = ?, employee_id = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.year, self.summary, self.employee_id, self.id))
            CONN.commit()

    def delete(self):
        """ Delete the table row corresponding to the current Review instance,
        delete the dictionary entry, and reassign id attribute. """
        if self.id:
            sql = "DELETE FROM reviews WHERE id = ?"
            CURSOR.execute(sql, (self.id,))
            del Review.all[self.id]
            self.id = None
            CONN.commit()

    @classmethod
    def get_all(cls):
        """ Return a list containing one Review instance per table row. """
        sql = "SELECT * FROM reviews"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    # Property methods
    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if isinstance(value, int) and value >= 2000:
            self._year = value
        else:
            raise ValueError("Year must be an integer greater than or equal to 2000.")

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        if isinstance(value, str) and value.strip():
            self._summary = value
        else:
            raise ValueError("Summary must be a non-empty string.")

    @property
    def employee_id(self):
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
        if isinstance(value, int):
            self._employee_id = value
        else:
            raise ValueError("Employee ID must be an integer.")