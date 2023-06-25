class EnvVarKeys:
    RedisHost = "REDIS_HOST"
    RedisPort = "REDIS_PORT"

    RedisValidationCodeDB = "REDIS_VALIDATION_CODE_DB"
    RedisRegistrationTokenDB = "REDIS_REGISTRATION_TOKEN_DB"
    RedisAttemptsDB = "REDIS_ATTEMPTS_DB"
    BlockedDB = "REDIS_BLOCKED_DB"

    GeneratedCodeTimeToLive = "GENERATED_CODE_TIME_TO_LIVE"
    RegistrationTokenTimeToLive = "REGISTRATION_TOKEN_TIME_TO_LIVE"
    AttemptsTimeToLive = "ATTEMPTS_TIME_TO_LIVE"
    BlockedKeyTimeToLive = "BLOCKED_KEY_TIME_TO_LIVE"

    MaximumCodeRequestCount = "MAXIMUM_CODE_REQUEST_COUNT"

    GenerateFakeCode = "GENERATE_FAKE_CODE"
