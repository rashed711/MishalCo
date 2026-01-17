<?php
// header('Content-Type: application/json');

require_once 'smtp_mailer.php';

// Configuration
$smtp_host = 'mail.mishal-lawfirm.com';
$smtp_user = 'noreply@mishal-lawfirm.com';
$smtp_pass = 'Aa@01028855';
$smtp_port = 465;

// Receiving email
// Receiving email
$receiving_email_address = ['Rashed1711@gmail.com', 'Rashed7271@gmail.com'];

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    // Sanitize input
    $name = strip_tags(trim($_POST["name"]));
    $phone = strip_tags(trim($_POST["phone"]));
    $message = strip_tags(trim($_POST["message"]));

    // Validation
    if (empty($name) || empty($phone) || empty($message)) {
        // http_response_code(400);
        echo "Please fill in all required fields.";
        exit;
    }

    // Email Subject
    $subject = "شكوى / استفسار جديد من: $name";

    // Email Content
    $email_content = "<h2>تفاصيل الشكوى / الاستفسار</h2>";
    $email_content .= "<p><strong>الاسم:</strong> $name</p>";
    $email_content .= "<p><strong>رقم الجوال:</strong> $phone</p>";
    $email_content .= "<p><strong>تفاصيل المشكلة / الاستفسار:</strong><br>$message</p>";

    // Attempt sending
    try {
        $mailer = new SMTPMailer($smtp_host, $smtp_user, $smtp_pass, $smtp_port);
        // Send email
        $mailer->send($receiving_email_address, $subject, $email_content, $name);

        echo "OK";
    } catch (Exception $e) {
        // http_response_code(500);
        echo "حدث خطأ أثناء الإرسال: " . $e->getMessage();
    }

} else {
    http_response_code(403);
    echo "There was a problem with your submission, please try again.";
}
?>