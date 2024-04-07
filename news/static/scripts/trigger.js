document.addEventListener('DOMContentLoaded', function() {
    function executePythonScript() {
        fetch('/execute-python-script/')  // Replace with the URL of your Django endpoint
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to execute Python script');
                }
                console.log('Python script executed successfully');
            })
            .catch(error => {
                console.error('Error executing Python script:', error);
            });

        setTimeout(function() {
        //your code to be executed after 1 second
        }, 5000);


    }
});