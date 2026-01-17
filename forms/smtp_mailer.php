<?php

class SMTPMailer
{
    private $host;
    private $username;
    private $password;
    private $port;
    private $timeout = 30;
    private $newline = "\r\n";
    private $socket;

    public function __construct($host, $username, $password, $port = 465)
    {
        $this->host = $host;
        $this->username = $username;
        $this->password = $password;
        $this->port = $port;
    }

    private function getLogHeader()
    {
        return "[SMTPMailer] ";
    }

    private function log($message)
    {
        // Uncomment the line below for debugging purposes
        // file_put_contents('smtp_debug.log', $this->getLogHeader() . $message . PHP_EOL, FILE_APPEND);
    }

    private function sendCommand($command, $expectCode)
    {
        $this->log("CLIENT: $command");
        fputs($this->socket, $command . $this->newline);
        $response = $this->readResponse();
        $this->log("SERVER: $response");

        $code = substr($response, 0, 3);
        if ($code != $expectCode) {
            throw new Exception("SMTP Error: Expected $expectCode, got $code. Response: $response");
        }
        return $response;
    }

    private function readResponse()
    {
        $response = "";
        while ($str = fgets($this->socket, 515)) {
            $response .= $str;
            if (substr($str, 3, 1) == " ") {
                break;
            }
        }
        return $response;
    }

    public function send($to, $subject, $body, $fromName = 'Website Contact')
    {
        try {
            // Determine protocol prefix based on port
            $protocol = '';
            if ($this->port == 465) {
                $protocol = 'ssl://';
            } else if ($this->port == 587) {
                $protocol = 'tls://';
            }

            $this->log("Connecting to $protocol{$this->host}:{$this->port}...");

            $this->socket = fsockopen($protocol . $this->host, $this->port, $errno, $errstr, $this->timeout);

            if (!$this->socket) {
                throw new Exception("Could not connect to SMTP host: $errno - $errstr");
            }

            $this->readResponse(); // Read initial server greeting

            $this->sendCommand('EHLO ' . $_SERVER['SERVER_NAME'], 250);

            // Authentication
            $this->sendCommand('AUTH LOGIN', 334);
            $this->sendCommand(base64_encode($this->username), 334);
            $this->sendCommand(base64_encode($this->password), 235);

            // Mail transaction
            $this->sendCommand("MAIL FROM: <{$this->username}>", 250);

            // Handle multiple recipients
            $recipients = [];
            if (is_array($to)) {
                $recipients = $to;
            } else {
                // Split by comma if string
                $recipients = array_map('trim', explode(',', $to));
            }

            foreach ($recipients as $recipient) {
                if (!empty($recipient)) {
                    $this->sendCommand("RCPT TO: <$recipient>", 250);
                }
            }
            $this->sendCommand('DATA', 354);

            // Headers
            // Format To header with all recipients
            $toString = implode(', ', $recipients);

            $headers = "MIME-Version: 1.0" . $this->newline;
            $headers .= "Content-type: text/html; charset=UTF-8" . $this->newline;
            $headers .= "From: =?UTF-8?B?" . base64_encode($fromName) . "?= <{$this->username}>" . $this->newline;
            $headers .= "Reply-To: =?UTF-8?B?" . base64_encode($fromName) . "?= <{$this->username}>" . $this->newline;
            $headers .= "To: $toString" . $this->newline;
            $headers .= "Subject: =?UTF-8?B?" . base64_encode($subject) . "?=" . $this->newline;
            $headers .= "X-Mailer: PHP/" . phpversion();

            // Send Body
            fputs($this->socket, $headers . $this->newline . $this->newline . $body . $this->newline . "." . $this->newline);

            $response = $this->readResponse();
            $this->log("SERVER (DATA End): $response");

            if (substr($response, 0, 3) != '250') {
                throw new Exception("Failed to send data. Server said: $response");
            }

            $this->sendCommand('QUIT', 221);
            fclose($this->socket);

            return true;

        } catch (Exception $e) {
            $this->log("Exception: " . $e->getMessage());
            if (is_resource($this->socket)) {
                fclose($this->socket);
            }
            // Re-throw so caller knows it failed
            throw $e;
        }
    }
}
?>