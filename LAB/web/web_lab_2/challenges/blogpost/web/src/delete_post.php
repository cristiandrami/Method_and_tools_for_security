<?php
	session_start();

	require_once 'user.php';


	if (!isset($_SESSION['uid'])) {
	    // The user is not authenticated, redirect to the login page
	    header("Location: login.php");
	    exit;
	}

	$host = getenv('DATABASE_HOST');
	$db   = 'blog';
	$dbuser = 'bloguser';
	$pass = 'blogpassword';
	$charset = 'utf8mb4';

	$dsn = "mysql:host=$host;dbname=$db;charset=$charset";
	$opt = [
	    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
	    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
	    PDO::ATTR_EMULATE_PREPARES   => false,
	];
	$pdo = new PDO($dsn, $dbuser, $pass, $opt);
        $user = new User($dsn, $dbuser, $pass, $opt);
        $user->loadFromSession();


 if (isset($_POST['post_id'])) {

    if (!$user->is_admin) {
         echo 'error';
        exit;
    }
    
    $post_id = $_POST['post_id'];

    $result = $pdo->query("DELETE FROM post WHERE id = '$post_id'");

    if ($result) {
        echo 'success';
    } else {
        // In the case of error, return the database error information for the learning purpose
        echo 'Failed to delete post: ' . $db->error;
    }
} else {
    echo 'error';
}
?>

