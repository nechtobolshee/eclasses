from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from english.models import Class, Lessons
from users.models import User
from english import calendar
from unittest.mock import patch


class ClassesForStudent(APITestCase):
    fixtures = ["english/tests/fixtures.json"]

    def setUp(self):
        self.student = User.objects.get(id=1)
        self.teacher = User.objects.get(id=2)

    def test_get_classes_list(self):
        self.client.force_login(user=self.student)
        expected_data = {
            "pk": 1,
            "name": "FirstClass",
            "students": [
                {"pk": 3, "first_name": "Ayden", "last_name": "Henris"},
                {"pk": 4, "first_name": "Damian", "last_name": "Ward"},
                {"pk": 5, "first_name": "Jonah", "last_name": "Matthews"},
                {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"}
            ],
            "teacher": {"pk": 2, "first_name": "Matthew", "last_name": "Becher"},
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "18:00:00",
            "end_time": "19:30:00"
        }
        url = reverse("classes-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertDictEqual(dict(response.data[0]), expected_data)

    def test_get_classes_success(self):
        self.client.force_login(user=self.student)
        expected_data = {
            "pk": 1,
            "name": "FirstClass",
            "students": [
                {"pk": 3, "first_name": "Ayden", "last_name": "Henris"},
                {"pk": 4, "first_name": "Damian", "last_name": "Ward"},
                {"pk": 5, "first_name": "Jonah", "last_name": "Matthews"},
                {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"}
            ],
            "teacher": {"pk": 2, "first_name": "Matthew", "last_name": "Becher"},
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "18:00:00",
            "end_time": "19:30:00"
        }
        url = reverse("student-classes-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertDictEqual(dict(response.data[0]), expected_data)

    def test_get_classes_failed(self):
        self.client.force_login(user=self.teacher)
        url = reverse("student-classes-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_leave_class(self):
        self.client.force_login(user=self.student)

        self.assertIn(self.student, Class.objects.get(pk=1).students.all())

        url = reverse("join-to-class", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertNotIn(self.student, Class.objects.get(pk=1).students.all())

    def test_join_class(self):
        self.client.force_login(user=self.student)
        data = {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"}

        self.assertNotIn(self.student, Class.objects.get(pk=3).students.all())

        url = reverse("join-to-class", kwargs={"pk": 3})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(data, response.data["students"])

        self.assertIn(self.student, Class.objects.get(pk=3).students.all())


class ClassesForTeacher(APITestCase):
    fixtures = ["english/tests/fixtures.json"]

    def setUp(self):
        self.student = User.objects.get(id=1)
        self.teacher = User.objects.get(id=2)

    def test_get_classes_success(self):
        self.client.force_login(user=self.teacher)
        expected_data = {
            "pk": 1,
            "name": "FirstClass",
            "students": [
                {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"},
                {"pk": 3, "first_name": "Ayden", "last_name": "Henris"},
                {"pk": 4, "first_name": "Damian", "last_name": "Ward"},
                {"pk": 5, "first_name": "Jonah", "last_name": "Matthews"}
            ],
            "teacher": {"pk": 2, "first_name": "Matthew", "last_name": "Becher"},
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "18:00:00",
            "end_time": "19:30:00"
        }
        url = reverse("teacher-classes-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertDictEqual(dict(response.data[0]), expected_data)

    def test_get_classes_failed(self):
        self.client.force_login(user=self.student)
        url = reverse("teacher-classes-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_search_classes_success(self):
        self.client.force_login(user=self.teacher)
        expected_data = {
            "pk": 1,
            "name": "FirstClass",
            "students": [
                {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"},
                {"pk": 3, "first_name": "Ayden", "last_name": "Henris"},
                {"pk": 4, "first_name": "Damian", "last_name": "Ward"},
                {"pk": 5, "first_name": "Jonah", "last_name": "Matthews"}
            ],
            "teacher": {"pk": 2, "first_name": "Matthew", "last_name": "Becher"},
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "18:00:00",
            "end_time": "19:30:00"
        }
        url = f'{reverse("classes-list")}?name=FirstClass&teacher=2&students=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertDictEqual(dict(response.data[0]), expected_data)

    def test_search_classes_success_empty_results(self):
        self.client.force_login(user=self.teacher)
        url = f'{reverse("classes-list")}?name=LostClass'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_class_success(self):
        self.client.force_login(user=self.teacher)
        expected_data = {
            "pk": 1,
            "name": "FirstClass",
            "students": [
                {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"},
                {"pk": 3, "first_name": "Ayden", "last_name": "Henris"},
                {"pk": 4, "first_name": "Damian", "last_name": "Ward"},
                {"pk": 5, "first_name": "Jonah", "last_name": "Matthews"}
            ],
            "teacher": {"pk": 2, "first_name": "Matthew", "last_name": "Becher"},
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "18:00:00",
            "end_time": "19:30:00"
        }
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(dict(response.data), expected_data)

    def test_get_class_failed(self):
        self.client.force_login(user=self.student)
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_class_success(self):
        self.client.force_login(user=self.teacher)
        data = {
            "name": "UpdatedFirstClass",
            "days": [1, 2],
            "start_time": "20:00:00",
            "end_time": "21:30:00"
        }
        expected_data = {
            "pk": 1,
            "name": "UpdatedFirstClass",
            "students": [
                {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"},
                {"pk": 3, "first_name": "Ayden", "last_name": "Henris"},
                {"pk": 4, "first_name": "Damian", "last_name": "Ward"},
                {"pk": 5, "first_name": "Jonah", "last_name": "Matthews"}
            ],
            "teacher": {"pk": 2, "first_name": "Matthew", "last_name": "Becher"},
            "days": ["Tuesday", "Wednesday"],
            "start_time": "20:00:00",
            "end_time": "21:30:00"
        }
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(dict(response.data), expected_data)

    def test_update_class_failed_403(self):
        self.client.force_login(user=self.student)
        data = {
            "name": "FailedUpdateFirstClass",
            "days": [3, 5]
        }
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_class_failed_incorrect_time(self):
        self.client.force_login(user=self.teacher)
        data = {
            "name": "FirstClass",
            "start_time": "22:00:00",
            "end_time": "20:00:00"
        }
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The start time can't be greater than the end time.", response.data["non_field_errors"])

    def test_update_class_failed_unfilled_time(self):
        self.client.force_login(user=self.teacher)
        data = {
            "name": "FirstClass",
            "end_time": "20:00:00"
        }
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Please, fill in the start and end times.", response.data["non_field_errors"])

    def test_delete_class_success(self):
        self.client.force_login(user=self.teacher)

        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Class.objects.filter(pk=1).exists())

    def test_delete_class_failed(self):
        self.client.force_login(user=self.student)
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_class_success(self):
        self.client.force_login(user=self.teacher)
        data = {
            "name": "NewClass",
            "students": [4, 5],
            "days": [1, 2],
            "start_time": "16:00:00",
            "end_time": "18:00:00"
        }
        expected_data = {
            "pk": 4,
            "name": "NewClass",
            "students": [
                {"pk": 4, "first_name": "Damian", "last_name": "Ward"},
                {"pk": 5, "first_name": "Jonah", "last_name": "Matthews"}
            ],
            "teacher": {"pk": 2, "first_name": "Matthew", "last_name": "Becher"},
            "days": ["Tuesday", "Wednesday"],
            "start_time": "16:00:00",
            "end_time": "18:00:00"
        }
        url = reverse("teacher-classes-list-create")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, response.data)

    def test_create_class_failed_403(self):
        self.client.force_login(user=self.student)
        data = {
            "name": "NewSecondClass",
            "students": [4, 5],
            "days": [1, 2],
            "start_time": "16:00:00",
            "end_time": "18:00:00"
        }

        url = reverse("teacher-classes-list-create")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_class_failed_incorrect_time(self):
        self.client.force_login(user=self.teacher)
        data = {
            "name": "NewSecondClass",
            "students": [4, 5],
            "days": [1, 2],
            "start_time": "20:00:00",
            "end_time": "18:00:00"
        }
        url = reverse("teacher-classes-list-create")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The start time can't be greater than the end time.", response.data["non_field_errors"])


class LessonsForStudent(APITestCase):
    fixtures = ["english/tests/fixtures.json"]

    def setUp(self):
        self.student = User.objects.get(id=1)
        self.teacher = User.objects.get(id=2)

    def test_get_lessons_success(self):
        self.client.force_login(user=self.student)
        expected_data = {
            "pk": 1,
            "class_name": "FirstClass",
            "status": "COMING",
            "start_time": "2030-07-04T01:14:43",
            "end_time": "2030-10-30T01:14:46"
        }
        url = reverse("student-lessons-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertDictEqual(dict(response.data[0]), expected_data)

    def test_get_lessons_failed(self):
        self.client.force_login(user=self.teacher)
        url = reverse("student-lessons-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LessonsForTeacher(APITestCase):
    fixtures = ["english/tests/fixtures.json"]

    def setUp(self):
        self.student = User.objects.get(id=1)
        self.teacher = User.objects.get(id=2)

    def test_get_lessons_success(self):
        self.client.force_login(user=self.teacher)
        expected_data = {
            "pk": 1,
            "class_name": "FirstClass",
            "status": "COMING",
            "start_time": "2030-07-04T01:14:43",
            "end_time": "2030-10-30T01:14:46"
        }
        url = reverse("teacher-lessons-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertDictEqual(dict(response.data[0]), expected_data)

    def test_get_lessons_failed(self):
        self.client.force_login(user=self.student)
        url = reverse("teacher-lessons-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_lesson_success(self):
        self.client.force_login(user=self.teacher)
        expected_data = {
            "pk": 1,
            "class_name": "FirstClass",
            "status": "COMING",
            "start_time": "2030-07-04T01:14:43",
            "end_time": "2030-10-30T01:14:46"
        }
        url = reverse("teacher-lesson-retrive-update", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertDictEqual(dict(response.data), expected_data)

    def test_get_lesson_failed(self):
        self.client.force_login(user=self.student)
        url = reverse("teacher-lesson-retrive-update", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('english.calendar.update_calendar_event')
    def test_update_lesson_success(self, mock_calendar_update):
        self.client.force_login(user=self.teacher)
        data = {
            "start_time": "2035-07-04T01:14:43",
            "end_time": "2036-10-30T01:14:46"
        }
        expected_data = {
            "pk": 1,
            "class_name": "FirstClass",
            "status": "COMING",
            "start_time": "2035-07-04T01:14:43",
            "end_time": "2036-10-30T01:14:46"
        }
        url = reverse("teacher-lesson-retrive-update", kwargs={"pk": 1})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(dict(response.data), expected_data)
        mock_calendar_update.assert_called_once()

    @patch('english.calendar.delete_calendar_event')
    def test_update_lesson_success_second(self, mock_calendar_delete):
        self.client.force_login(user=self.teacher)
        data = {
            "status": "CANCELED",
            "start_time": "2030-07-04T01:14:43",
            "end_time": "2032-10-30T01:14:46"
        }
        expected_data = {
            "pk": 1,
            "class_name": "FirstClass",
            "status": "CANCELED",
            "start_time": "2030-07-04T01:14:43",
            "end_time": "2032-10-30T01:14:46"
        }
        url = reverse("teacher-lesson-retrive-update", kwargs={"pk": 1})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(dict(response.data), expected_data)
        mock_calendar_delete.assert_called()

    def test_update_lesson_failed_incorrect_time_1(self):
        self.client.force_login(user=self.teacher)
        data = {
            "start_time": "2050-07-04T01:14:43",
            "end_time": "2030-10-30T01:14:46"
        }
        url = reverse("teacher-lesson-retrive-update", kwargs={"pk": 1})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("The start time can't be greater than the end time.", response.data["detail"][0])

    def test_update_lesson_failed_incorrect_time_2(self):
        self.client.force_login(user=self.teacher)
        data = {
            "start_time": "2050-07-04T01:14:43"
        }
        url = reverse("teacher-lesson-retrive-update", kwargs={"pk": 1})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("Please, fill in the start and end times.", response.data["detail"][0])

    def test_update_lesson_failed_403(self):
        self.client.force_login(user=self.student)
        data = {
            "start_time": "2030-07-04T01:14:43",
            "end_time": "2032-10-30T01:14:46"
        }
        url = reverse("teacher-lesson-retrive-update", kwargs={"pk": 1})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_lesson_failed_status(self):
        self.client.force_login(user=self.teacher)
        data = {
            "status": "PROGRESS"
        }
        url = reverse("teacher-lesson-retrive-update", kwargs={"pk": 1})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("Lesson status can be changed only to CANCELED.", response.data["status"])

    @patch('english.calendar.create_calendar_event', return_value="google_id")
    def test_create_lesson_success(self, mock_calendar_insert):
        self.client.force_login(user=self.teacher)
        data = {
            "class_name": 1,
            "status": "COMING",
            "start_time": "2040-07-04T01:14:43",
            "end_time": "2042-10-30T01:14:46"
        }
        expected_data = {
            "pk": 3,
            "class_name": "FirstClass",
            "status": "COMING",
            "start_time": "2040-07-04T01:14:43",
            "end_time": "2042-10-30T01:14:46"
        }
        url = reverse("teacher-lessons-list-create")

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_data, response.data)
        mock_calendar_insert.assert_called_once()
        lesson = Lessons.objects.get(pk=response.data["pk"])
        self.assertEqual(lesson.google_event_id, "google_id")

    def test_create_lesson_failed_403(self):
        self.client.force_login(user=self.student)
        data = {
            "class_name": 1,
            "status": "COMING",
            "start_time": "2040-07-04T01:14:43",
            "end_time": "2042-10-30T01:14:46"
        }
        url = reverse("teacher-lessons-list-create")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_lesson_failed_incorrect_time(self):
        self.client.force_login(user=self.teacher)
        data = {
            "class_name": 1,
            "status": "COMING",
            "start_time": "2010-07-04T01:14:43",
            "end_time": "2015-07-04T01:14:43",
        }
        url = reverse("teacher-lessons-list-create")
        response = self.client.post(url, data=data)
        self.assertEqual("Start time should be larger than current time.", response.data["start_time"][0])

    def test_create_lesson_failed_incorrect_time_2(self):
        self.client.force_login(user=self.teacher)
        data = {
            "class_name": 1,
            "status": "COMING",
            "start_time": "2040-07-04T01:14:43",
            "end_time": "2030-07-04T01:14:43",
        }
        url = reverse("teacher-lessons-list-create")
        response = self.client.post(url, data=data)
        self.assertEqual("The start time can't be greater than the end time.", response.data["detail"][0])
