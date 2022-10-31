//const winston = require('winston');
const { createLogger, format, transports } = require("winston");
const { combine, timestamp, label, prettyPrint } = format;
const config = require("config");
const logger_config = config.get("logger");

const logConfiguration = {
  format: combine(label({ label: "main module" }), timestamp(), prettyPrint()),
  transports: [
    // save to console
    new transports.Console({ level: logger_config.console_level }),
    // save to file
    new transports.File({
      filename: logger_config.file_name,
      level: logger_config.file_level,
    }),
  ],
};

const logger = createLogger(logConfiguration);

module.exports.logger = logger;
