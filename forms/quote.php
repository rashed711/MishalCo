<?php
  /**
  * Requires the "PHP Email Form" library
  * The "PHP Email Form" library is available only in the pro version of the template
  * The library should be uploaded to: vendor/php-email-form/php-email-form.php
  * For more info and help: https://bootstrapmade.com/php-email-form/
  */

  // Replace contact@example.com with your real receiving email address
  $receiving_email_address = 'Rashed1711@gmail.com';

  if( file_exists($php_email_form = '../assets/vendor/php-email-form/php-email-form.php' )) {
    include( $php_email_form );
  } else {
    // Fallback: simple mail() when php-email-form library is missing.
    function safe_post_q($k) {
      return isset($_POST[$k]) ? trim(strip_tags($_POST[$k])) : '';
    }

    $name = safe_post_q('name');
    $email = safe_post_q('email');
    $phone = safe_post_q('phone');
    $subject = 'Request for a quote';
    $message = safe_post_q('message');

    $headers = "From: " . ($name ?: 'Website Contact') . " <" . ($email ?: 'no-reply@example.com') . ">\r\n";
    if ($email) { $headers .= "Reply-To: " . $email . "\r\n"; }
    $body = "Name: $name\nEmail: $email\nPhone: $phone\n\nMessage:\n$message\n";

    $sent = false;
    try {
      $sent = @mail($receiving_email_address, $subject, $body, $headers);
    } catch (Exception $e) {
      $sent = false;
    }

    echo $sent ? 'OK' : 'ERROR';
    exit;
  }

  $contact = new PHP_Email_Form;
  $contact->ajax = true;
  
  $contact->to = $receiving_email_address;
  $contact->from_name = $_POST['name'];
  $contact->from_email = $_POST['email'];
  $contact->subject = 'Request for a quote';

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
  $contact->add_message( $_POST['phone'], 'Phone');
  $contact->add_message( $_POST['message'], 'Message', 10);

  echo $contact->send();
?>
