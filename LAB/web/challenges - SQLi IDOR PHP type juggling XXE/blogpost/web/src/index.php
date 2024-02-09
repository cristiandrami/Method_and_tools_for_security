<?php
     session_start();
     require_once('user.php');
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
	if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	    // The request is a form submission
	    $title = $_POST['title'];
	    $content = $_POST['content'];
	    $id = rand(1, 10000);  // Generate a random id between 1 and 1000

	    $sql = "INSERT INTO post (id, title, content) VALUES (?, ?, ?)";
	    $stmt = $pdo->prepare($sql);
	    $stmt->execute([$id, $title, $content]);

	    // Redirect to the new post
	    header("Location: post.php?id=" . $id);
	    exit;
	}

	$sql = "SELECT id, title, content FROM post WHERE id < 10001";
	$stmt = $pdo->prepare($sql);
	$stmt->execute();
	$posts = $stmt->fetchAll();

        if (isset($_GET['logout'])) {
	    $user->logout();
	    header('Location: login.php'); // Redirect to login page after logout
            exit;
	}
?>

<!DOCTYPE html>
<html>
<head>
  <title>Blog</title>
  <link href="css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="./css/styles.css">
</head>
<body>
  <div class="container mt-4">
    <h1 class="text-center">Welcome to our Blog!</h1>

        <div class="container">
            <?php
                if ($user->authorized):
            ?>
              <h2 class="text-center">Welcome, <?=$user->username;?>! Click here to <a href="index.php?logout">Logout</a> </h2>
        <?php endif; ?>
        </div>    

<h2>Create a new post</h2>
    <form method="POST">
      <div class="form-group">
        <label for="title">Title</label>
        <input type="text" class="form-control" id="title" name="title" required>
      </div>
      <div class="form-group">
        <label for="content">Content</label>
        <textarea class="form-control" id="content" name="content" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>

    <h2 class="mt-4">All posts</h2>
    <?php foreach ($posts as $post): ?>
    <div class="card mt-4" id="post-<?= $post['id'] ?>">
      <div class="card-body">
        <img class="card-img-top post-image" src="images/icon.png" alt="Card image cap">
        <h5 class="card-title"><a href="post.php?id=<?= $post['id'] ?>"><?= htmlspecialchars($post['title']) ?></a></h5>
        <p class="card-text"><?= substr(htmlspecialchars($post['content']), 0, 100) ?>...</p>
	<?php if ($user->is_admin): ?>
	    <button onclick="deletePost(<?=$post['id'];?>)">Delete</button>
	<?php endif; ?>
      </div>
    </div>
    <?php endforeach; ?>
  </div>

<script>
function deletePost(postId) {
    $.ajax({
        url: 'delete_post.php',
        type: 'POST',
        data: {
            'post_id': postId
        },
        success: function(response) {
            if (response.trim() == 'success') {
                alert('Post deleted successfully');
                $('#post-' + postId).remove();
	    } else {
                alert('Failed to delete post');
            }
        }
    });
}
</script>
  <script src="js/jquery-3.5.1.min.js"></script>
</body>
</html>

