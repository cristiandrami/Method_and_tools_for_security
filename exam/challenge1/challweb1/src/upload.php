
<?php

function file_mime_type($file) {
  if (function_exists('mime_content_type')) {
    $file_type = @mime_content_type($file);
    if (strlen($file_type) > 0) {
        return $file_type;
    }
  }
}

function check_file_type($file) {
    $mime_type = file_mime_type($file);
    if ($mime_type === false || strpos($mime_type, 'image/') !== 0) {
        return false;
    }
    return true;
}

function is_valid_image_extension($filename) {
    $valid_extensions = ['jpg', 'jpeg', 'png', 'gif'];
    $extension = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
    return in_array($extension, $valid_extensions);
}


if (isset($_FILES['image'])) {
    $file = $_FILES['image'];

    // Check if the file is an image
    if (check_file_type($file['tmp_name']) && is_valid_image_extension($file['name'])) {
        $upload_dir = 'uploads/';
        $upload_file = $upload_dir . basename($file['name']);

        if (move_uploaded_file($file['tmp_name'], $upload_file)) {
            echo "File is valid, and was successfully uploaded. Refresh the gallery!\n";
        } 
    } else {
        echo "File is not an image. What are you trying to do?\n";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Your Image</title>
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/style.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1 class="text-center">Image Upload Form</h1>
        <form action="upload.php" method="post" enctype="multipart/form-data">
            <div class="mb-3">
                <label for="image" class="form-label">Select image to upload:</label>
                <input type="file" class="form-control" id="image" name="image">
            </div>
            <button type="submit" class="btn btn-primary">Upload Image</button>
        </form>
    </div>
    <script src="js/bootstrap.bundle.min.js"></script>
</body>
</html>

