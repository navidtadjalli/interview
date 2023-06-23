# def test_if_request_attempts_for_phone_number_saves_into_redis(self):
#     self.delete_redis_keys()
#     fake_code = True
#
#     create_validation_code(self.phone_numbers[0], self.ips[0])
#     redis_value: bytes = validation_code_redis.get(self.phone_number_attempts_keys[0])
#     redis_value_decoded: str = redis_value.decode(encoding='utf-8')
#
#     self.assertEqual(redis_value_decoded, "1")
#
#
# def test_if_request_attempts_for_phone_number_increases_on_request(self):
#     self.delete_redis_keys()
#     fake_code = True
#
#     create_validation_code(self.phone_numbers[0], self.ips[0])
#     create_validation_code(self.phone_numbers[0], self.ips[0])
#     redis_value: bytes = validation_code_redis.get(self.phone_number_attempts_keys[0])
#     redis_value_decoded: str = redis_value.decode(encoding='utf-8')
#
#     self.assertEqual(redis_value_decoded, "2")
#
#
# def test_if_request_attempts_count_for_phone_number_get_checked(self):
#     self.delete_redis_keys()
#     fake_code = True
#
#     create_validation_code(self.phone_numbers[0], self.ips[0])
#     create_validation_code(self.phone_numbers[0], self.ips[0])
#     create_validation_code(self.phone_numbers[0], self.ips[0])
#
#     with self.assertRaises(exceptions.MaximumPhoneNumberAttemptException):
#         create_validation_code(self.phone_numbers[0], self.ips[0])
#
#
# def test_if_different_attempts_from_different_ips_increases_phone_number_attempts(self):
#     self.delete_redis_keys()
#     fake_code = True
#
#     create_validation_code(self.phone_numbers[0], self.ips[0])
#     create_validation_code(self.phone_numbers[0], self.ips[1])
#     create_validation_code(self.phone_numbers[0], self.ips[2])
#
#     with self.assertRaises(exceptions.MaximumPhoneNumberAttemptException):
#         create_validation_code(self.phone_numbers[0], self.ips[3])
#
#
# def test_if_request_attempts_for_ip_saves_into_redis(self):
#     self.delete_redis_keys()
#     fake_code = True
#
#     create_validation_code(self.phone_numbers[0], self.ips[0])
#     redis_value: bytes = validation_code_redis.get(self.ip_attempts_keys[0])
#     redis_value_decoded: str = redis_value.decode(encoding='utf-8')
#
#     self.assertEqual(redis_value_decoded, "1")
#
#
# def test_if_request_attempts_for_ip_increases_on_request(self):
#     self.delete_redis_keys()
#     fake_code = True
#
#     create_validation_code(self.phone_numbers[0], self.ips[0])
#     create_validation_code(self.phone_numbers[0], self.ips[0])
#     redis_value: bytes = validation_code_redis.get(self.ip_attempts_keys[0])
#     redis_value_decoded: str = redis_value.decode(encoding='utf-8')
#
#     self.assertEqual(redis_value_decoded, "2")
#
#
# def test_if_request_attempts_count_for_ip_get_checked(self):
#     self.delete_redis_keys()
#     fake_code = True
#
#     create_validation_code(self.phone_numbers[0], self.ips[0])
#     create_validation_code(self.phone_numbers[0], self.ips[0])
#     create_validation_code(self.phone_numbers[1], self.ips[0])
#
#     with self.assertRaises(exceptions.MaximumIPAttemptException):
#         create_validation_code(self.phone_numbers[2], self.ips[0])
#
#
# def test_if_different_attempts_from_one_ip_and_different_phone_numbers_gets_checked(self):
#     self.delete_redis_keys()
#     fake_code = True
#
#     create_validation_code(self.phone_numbers[0], self.ips[0])
#     create_validation_code(self.phone_numbers[1], self.ips[0])
#     create_validation_code(self.phone_numbers[2], self.ips[0])
#
#     with self.assertRaises(exceptions.MaximumIPAttemptException):
#         create_validation_code(self.phone_numbers[3], self.ips[0])
#
# # postponing remaining tests after middleware created
# # attempts ttl
# # def test_if_phone_number_get_blocked_after_three_times(self):
# # def test_if_ip_get_blocked_after_three_times(self):
# # def test_if_request_blocked_ips_has_ttl(self):
# # def test_if_attempts_count_get_deleted_after_successful_validation
