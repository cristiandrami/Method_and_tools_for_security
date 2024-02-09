<?php
    session_start();  // Start the session
    if (!isset($_SESSION['uid']) || !isset($_SESSION['username'])) {
        // User is not logged in. Redirect them to the login page
        header("Location: login.php");
        exit;
    }

    $host = getenv('DATABASE_HOST');
    $db   = 'blog';
    $user = 'bloguser';
    $pass = 'blogpassword';
    $charset = 'utf8mb4';

    $dsn = "mysql:host=$host;dbname=$db;charset=$charset";
    $opt = [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => true,
     ];
    $pdo = new PDO($dsn, $user, $pass, $opt);

    // Check if the form has been submitted
    if (isset($_POST['new_title']) && $_SESSION['is_admin'] === 1) {
        $new_title = $_POST['new_title'];
        $post_id = $_GET['id'];
        $pdo->query("UPDATE post SET title = '$new_title' WHERE id = '$post_id'");
    }

    $sql = "SELECT id, title, content FROM post";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $posts = $stmt->fetchAll();

    $post = $posts[array_search($_GET['id'], array_column($posts, 'id'))];

    if ($_SESSION['is_admin'] === 1 && isset($_GET['preview'])) {
       $previewData = file_get_contents($_GET['preview']);
    }
?>

<!DOCTYPE html>
<html>
<head>
  <title><?= $post['title'] ?></title>
  <link href="css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="./css/styles.css">
</head>
<body>
<div class="container mt-4" id="<?= $post['id']?>">
    <div class="card">
      <div class="card-body">
        <img class="card-img-top post-image" src="images/icon.png" alt="Card image cap">
        <h1 class="card-title"><?= $post['title'] ?></h1>
        <p class="card-text"><?= $post['content'] ?></p>
        <!-- If admin, show the form to change title -->
        <?php if ($_SESSION['is_admin'] === 1): ?>
          <form action="" method="POST">
            <input type="text" name="new_title" placeholder="New title" required>
            <input type="submit" value="Change title">
          </form>
        <?php endif; ?>
      </div>
    </div>
    <?php if (isset($previewData)): ?>
    <div class="card mt-4">
      <div class="card-body">
        <p><?= $previewData ?></p>
      </div>
    </div>
    <?php endif; ?>
    <a href="index.php" class="btn btn-primary mt-4">Back to Home</a>
  </div>

  <script src="js/jquery-3.5.1.min.js"></script>
</body>
</html>

