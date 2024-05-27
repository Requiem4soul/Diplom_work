<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parking System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        #parking-image {
            display: block;
            margin: 20px auto;
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }
        #parking-info {
            text-align: center;
            color: #555;
            font-size: 18px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Parking System</h1>
        <img id="parking-image" src="get_image.php" alt="Parking Image">
        <div id="parking-info">Free Spots: <span id="free-spots">Loading...</span></div>
    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script>
        $(document).ready(function() {
            function updateData() {
                $.ajax({
                    url: 'get_data.php',
                    type: 'GET',
                    dataType: 'json',
                    success: function(data) {
                        $('#free-spots').text(data.free_spots);
                    },
                    error: function() {
                        $('#free-spots').text('Error');
                    }
                });

                // Update image
                var image = document.getElementById('parking-image');
                image.src = "get_image.php?random=" + new Date().getTime();
            }

            updateData(); // Update data on page load

            setInterval(updateData, 500); // Update data every 5 seconds
        });
    </script>
</body>
</html>
