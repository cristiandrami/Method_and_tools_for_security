<?php
    session_start();

    require('user.php');
    ob_start();
     
     $host = getenv('DATABASE_HOST');
     
     //******************************************  credenziali in CHIARO!!!!
     $db   = 'blog';
     $dbuser = 'bloguser';
     $pass = 'blogpassword';
     $charset = 'utf8mb4';
    /****************************************************************** */
     
    
    //************** PDO is a library that is used to use prepared statements */
      $dsn = "mysql:host=$host;dbname=$db;charset=$charset";
      $opt = [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ];
     $user = new User($dsn, $dbuser, $pass, $opt);

?>
<!-- doctype html -->
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Login</title>

        <link href="css/bootstrap.min.css" rel="stylesheet">
        <script src="js/jquery-3.3.1.slim.min.js"></script>
        <script src=css/bootstrap.min.js"></script>
    </head>

    <body>
        <div class="container">
            <?php
                if ($user->authorized):
            ?>
                    <h1>Welcome, <?=$user->username;?>!</h1>
            <?php
                elseif (isset($_GET['register'])):
            ?>
                <h2>Register</h2>
		<form method="POST" class="my-3"> 

             <?php 
	        if ($_SERVER['REQUEST_METHOD'] === 'POST' &&  isset($_POST['submitRegister']) && isset($_POST['username']) && isset($_POST['password'])) { 
	            if ($user->register($_POST['username'], $_POST['password'], $_POST['email'])){ 
    				exit;
		    }else{ 
              ?> 
	                <div class="alert alert-danger">User already registered!</div>
		<?php 
		     } 
                  }
		?>
                    <input type="text" name="username" class="form-control" placeholder="Username"/>
                    <input type="password" name="password" class="form-control mt-2" placeholder="Password"/>
		    <input type="email" name="email" class="form-control mt-2" placeholder="Email"/>
                    <button class="btn btn-primary mt-2" name="submitRegister">Register</button>
                </form>
                <div class="mt-3"><a href="./">Login</a> | <a href="?forgot">Forgot password?</a></div>
            <?php
                elseif (isset($_GET['forgot'])):
            ?>
                <h2>Reset password</h2>
                <form method="POST" class="my-3">
                    <?php if (isset($_POST['reset'])): ?>
                        <div class="alert alert-success">Email sent</div>
                    <?php endif; ?>
                    <input type="text" name="reset" class="form-control" placeholder="Username"/>
                    <button class="btn btn-primary mt-2">Reset</button>
                </form>
                <div class="mt-3"><a href="./">Login</a> | <a href="?register">Register</a></div>
            <?php
                else:
		  if (isset($_POST['submitLogin']) && $_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['username']) && isset($_POST['password'])) {
			    
            //****************** VEDERE CLASSE USER in user.php*/
            if ($user->login($_POST['username'], $_POST['password'])) {
			      //echo "<script>window.location.href='index.php';</script>";
    				exit;
			    } else{ ?>
	             
	                      <div class="alert alert-danger">Invalid login</div>
		<?php 
		     } 
                  }
		?>
                <h2>Login to your account</h2>
                <form method="POST" class="my-3">
                    <input type="text" name="username" class="form-control" placeholder="Username"/>
                    <input type="password" name="password" class="form-control mt-2" placeholder="Password"/>
                    <button class="btn btn-primary mt-2" name="submitLogin">Login</button>
                </form>
                <div class="mt-3"><a href="?forgot">Forgot password?</a> | <a href="?register">Register</a></div>
            <?php
               endif;
              ob_end_flush();
            ?>
        </div>
    </body>
</html>
