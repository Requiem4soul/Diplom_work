<?php
header("Content-type: image/jpeg");
header("Cache-Control: no-cache, must-revalidate"); // HTTP/1.1
header("Expires: Sat, 1 Jan 2000 00:00:00 GMT"); // Дата в прошлом для отключения кэширования

$servername = "localhost";
$username = "root";
$password = "";
$database = "parking_system";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT image_data FROM last_updated_image ORDER BY timestamp DESC LIMIT 1";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    echo $row["image_data"];
} else {
    echo "No image data available";
}

$conn->close();
?>
