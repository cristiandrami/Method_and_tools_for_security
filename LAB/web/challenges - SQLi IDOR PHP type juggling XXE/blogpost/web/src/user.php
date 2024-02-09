<?php
    class User {
        public $authorized = false;
        public $is_admin = false;
        public $uid;
        public $username;


        public function __construct($dsn, $db_user, $db_pass, $opt) {
            $this->db = new PDO($dsn, $db_user, $db_pass, $opt);

            if (isset($_SESSION['uid'])) {
                $this->authorized = true;
                $this->uid = $_SESSION['uid'];
                $this->username = $_SESSION['username'];
                $this->is_admin = $_SESSION['is_admin'];
            } else if (isset($_POST['reset'])) {
                $user = $_POST['reset'];
                $this->reset($user);
            } else if (isset($_POST['username']) && isset($_POST['password'])) {
                $user = $_POST['username'];
                $pass = $_POST['password'];
                $this->login($user, $pass);
            }
        }

	public function register($user, $pass, $email) {
	    // Check if username already exists
	    $st = $this->db->prepare('SELECT `uid` FROM users WHERE username = :u');
	    $st->execute(array(':u' => $user));
	    $row = $st->fetch();

	    // If the username is taken, return false
	    if ($row) {
		return false;
	    }

	    // Insert new user into database
            $st = $this->db->prepare('INSERT INTO users (username, password, email) VALUES (:u, :p, :e)');
            $result = $st->execute(array(':u' => $user, ':p' => sha1($pass), ':e' => $email));

	    // If the insert was successful, log in the new user
	    if ($result) {
		//echo "REGISTER FUNCTION BEFORE LOGIN -- user: $user, password: $pass <br>";
		$this->login($user, $pass);
	    }

	    // Return the result of the insert query
	    return $result;
	}

        public function login($user, $pass) {
            $st = $this->db->prepare('SELECT uid, username, password, is_admin
                    FROM users
                    WHERE username = :u');
	    $st->execute(array(':u' => $user));
	   // Add debug output here
	    if ($st->rowCount() === 0) {
		//echo 'No user with this username found';
		return false;
	    }

            $row = $st->fetch();

            if ($row && $row['password'] == sha1($pass)) {
                $this->authorized = true;
                $this->uid = $row['uid'];
                $_SESSION['uid'] = $this->uid;
                $this->username = $row['username'];
                $_SESSION['username'] = $this->username;
		$this->is_admin = $row['is_admin'];
		$_SESSION['is_admin'] = $this->is_admin;
		header("Location: index.php");
		exit;
            } else {
                return false;
            }
        }
	public function loadFromSession() {
	    if (isset($_SESSION['uid']) && isset($_SESSION['username'])) {
		$this->uid = $_SESSION['uid'];
		$this->username = $_SESSION['username'];
		$this->authorized = true;
	    }
	}

	public function logout() {
	    // Unset all session values 
	    $_SESSION = array();

	    // Destroy the session 
	    session_destroy();

	    $this->authorized = false;
	    $this->uid = null;
	    $this->username = null;
	}


        public function reset($user) {
            $st = $this->db->prepare('SELECT `uid`, `username`, `email`
                    FROM users
                    WHERE username = :u');
            $st->execute(array(':u' => $user));
            $row = $st->fetch();

            if ($row) {
                $token = $this->generateRequest();

                $st = $this->db->prepare('UPDATE users SET `reset` = :reset, password = 0 WHERE uid = :uid LIMIT 1');
                $status = $st->execute(array(':uid' => $row['uid'], ':reset' => $token));

                $body = "We received a request for your account details.<br/><br/>Username: {$row['username']}<br/>To reset your password, click on this link: <a href='http://www.example.org/?reset={$token}'>http://www.example.org/?reset={$token}</a>";

                $to = $row['email'];
                $subject = 'Password request';
                $from = 'no-reply@example.org';
                 
                // To send HTML mail, the Content-type header must be set
                $headers  = 'MIME-Version: 1.0' . "\r\n";
                $headers .= 'Content-type: text/html; charset=iso-8859-1' . "\r\n";
                 
                // Create email headers
                $headers .= 'From: '.$from."\r\n".
                            'Reply-To: '.$from."\r\n";


		               
		//mail($to, $subject, $body, $headers);
            }
        }

        private function generateRequest() {
            $token = md5(openssl_random_pseudo_bytes(32));
            return $token;
        }

    }
?>
