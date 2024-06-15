import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from my_contacts_api.app import models, schemas, crud
from my_contacts_api.app.database import SessionLocal

class TestCRUD(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = models.User(id=1, email="test@example.com")

    def test_create_user(self):
        user_data = schemas.UserCreate(email="test@example.com", password="password")
        result = crud.create_user(db=self.session, user=user_data)
        self.assertEqual(result.email, "test@example.com")
        self.assertTrue(hasattr(result, "id"))

    def test_get_user_by_email_found(self):
        user = models.User(id=1, email="test@example.com")
        self.session.query().filter().first.return_value = user
        result = crud.get_user_by_email(db=self.session, email="test@example.com")
        self.assertEqual(result, user)

    def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = crud.get_user_by_email(db=self.session, email="test@example.com")
        self.assertIsNone(result)

    def test_create_contact(self):
        contact_data = schemas.ContactCreate(name="Test Contact", email="contact@example.com", phone="123456789")
        result = crud.create_contact(db=self.session, contact=contact_data, user_id=self.user.id)
        self.assertEqual(result.name, "Test Contact")
        self.assertTrue(hasattr(result, "id"))

    def test_get_contacts(self):
        contacts = [models.Contact(), models.Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = crud.get_contacts(db=self.session, user_id=self.user.id, skip=0, limit=10)
        self.assertEqual(result, contacts)

if __name__ == '__main__':
    unittest.main()
