<?php
// Подключение к базе данных
$connection = mysqli_connect('localhost', 'root', '', 'parking_system');

// Запрос для получения последнего количества свободных мест
$query = "SELECT free_spots FROM parking_data ORDER BY timestamp DESC LIMIT 1";
$result = mysqli_query($connection, $query);
$data = mysqli_fetch_assoc($result);

// Возвращаем данные в формате JSON
echo json_encode($data);
?>
