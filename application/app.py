from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from mongoengine import Document, StringField, DateTimeField, NotUniqueError
from datetime import datetime
from .model import HealthCheckModel
import re

app = Flask(__name__)
api = Api(app)


class UserModel(Document):
    cpf = StringField(required=True, unique=True)
    email = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    birth_date = DateTimeField(required=True)


user_parser = reqparse.RequestParser()
user_parser.add_argument("cpf", type=str, required=True, help="CPF is required")
user_parser.add_argument("email", type=str, required=True, help="Email is required")
user_parser.add_argument(
    "first_name", type=str, required=True, help="First name is required"
)
user_parser.add_argument(
    "last_name", type=str, required=True, help="Last name is required"
)
user_parser.add_argument(
    "birth_date", type=str, required=True, help="Birth date is required"
)


class User(Resource):
    def validate_cpf(self, cpf):
        # Has the correct mask?
        if not re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf):
            return False

        # Grab only numbers
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Does it have 11 digits?
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Validate first digit after -
        sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validate second digit after -
        sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True

    def post(self):
        data = user_parser.parse_args()

        if not self.validate_cpf(data["cpf"]):
            return {"message": "CPF is invalid!"}, 400

        try:
            birth_date = datetime.strptime(data["birth_date"], "%Y-%m-%d")
        except ValueError:
            return {"message": "Birth date format is incorrect!"}, 400

        user = UserModel(
            cpf=data["cpf"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            birth_date=birth_date,
        )

        try:
            response = user.save()
            return {"message": f"User ID: {response.id} has been created"}, 201
        except NotUniqueError:
            return {"message": "CPF already exists in database"}, 400

    def get(self, cpf):
        response = UserModel.objects(cpf=cpf).first()

        if response:
            return {
                "cpf": response.cpf,
                "email": response.email,
                "first_name": response.first_name,
                "last_name": response.last_name,
                "birth_date": response.birth_date.strftime("%Y-%m-%d"),
            }, 200

        return {"message": "User does not exist in database!"}, 404

    def delete(self, cpf):
        response = UserModel.objects(cpf=cpf)
        if response:
            response.delete()
            return {"messsage": "User deleted"}, 204
        else:
            return {"message": "User does not exist in database!"}, 404


class Users(Resource):
    def get(self):
        return jsonify(UserModel.objects())


class HealthCheck(Resource):
    def get(self):
        response = HealthCheckModel(status="healthy").save()
        if response:
            return "Healthy", 200
        else:
            HealthCheckModel(status="healthy")
            return "Healthy", 200
