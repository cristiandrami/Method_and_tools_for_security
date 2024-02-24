<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Gallery</title>
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/style.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1 class="text-center">Welcome to the Image Gallery</h1>
        <p class="text-center">Upload your images and see them on display!</p>
        <div>
            <a href="upload.php" class="btn btn-primary">Upload Image</a>
        </div>
        <div class="gallery">
            <?php
            $files = glob("uploads/*.*");
            for ($i=0; $i<count($files); $i++) {
                $image = $files[$i];
                echo '<img src="'.$image .'" alt="Random image" class="img-responsive" />';
            }
            ?>
        </div>
    </div>
    <script src="js/bootstrap.bundle.min.js"></script>
</body>
</html>

