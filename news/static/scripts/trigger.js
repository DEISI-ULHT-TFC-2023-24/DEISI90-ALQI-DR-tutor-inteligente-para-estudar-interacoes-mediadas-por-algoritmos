document.addEventListener('DOMContentLoaded', function() {
    function executePythonScript() {
        fetch('/execute-python-script/')
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
        }, 5000);


    }
});