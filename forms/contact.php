<?php
  /**
  * Requires the "PHP Email Form" library-1
  * The "PHP Email Form" library is available only in the pro version of the template
  * The library should be uploaded to: vendor/php-email-form/php-email-form.php
  * For more info and help: https://bootstrapmade.com/php-email-form/
  */

  // Replace contact@example.com with your real receiving email address
  $receiving_email_address = 'Rashed1711@gmail.com';

  if( file_exists($php_email_form = '../assets/vendor/php-email-form/php-email-form.php' )) {
    include( $php_email_form );
  } else {
    // Fallback: use a simple PHP mail() implementation when the
    // php-email-form library is not available. This keeps the contact
    // form functional on hosts without the library.
    function safe_post($k) {
      return isset($_POST[$k]) ? trim(strip_tags($_POST[$k])) : '';
    }

    $name = safe_post('name');
    $email = safe_post('email');
    $subject = safe_post('subject') ?: 'Contact Form Message';
    $message = safe_post('message');

    $headers = "From: " . ($name ?: 'Website Contact') . " <" . ($email ?: 'no-reply@example.com') . ">\r\n";
    if ($email) {
      $headers .= "Reply-To: " . $email . "\r\n";
    }
    $body = "Name: $name\nEmail: $email\n\nMessage:\n$message\n";

    $sent = false;
    // Suppress warnings from mail and return a simple status string.
    try {
      $sent = @mail($receiving_email_address, $subject, $body, $headers);
    } catch (Exception $e) {
      $sent = false;
    }

    echo $sent ? 'OK' : 'ERROR';
    // Stop further execution since we've handled the send.
    exit;
  }

  $contact = new PHP_Email_Form;
  $contact->ajax = true;
  
  $contact->to = $receiving_email_address;
  $contact->from_name = $_POST['name'];
  $contact->from_email = $_POST['email'];
  $contact->subject = $_POST['subject'];

  // Uncomment below code if you want to use SMTP to send emails. You need to enter your correct SMTP credentials
  /*
  $contact->smtp = array(
    'host' => 'example.com',
    'username' => 'example',
    'password' => 'pass',
    'port' => '587'
  );
  */

  $contact->add_message( $_POST['name'], 'From');
  $contact->add_message( $_POST['email'], 'Email');
  $contact->add_message( $_POST['message'], 'Message', 10);

  echo $contact->send();
?>
