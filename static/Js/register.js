$(document).ready(function(){

    /// En este selector se valida que las contraseñas sean iguales
        $(".submit-btn").click(function(){
            var pass = $("#inputPass").val();
            console.log(pass);
            var passC = $("#inputCPass").val();
            console.log(passC);

            if(pass == passC && pass != "" && passC != ""){
                $("#formReg").trigger('click');
            }else{
                alert("Las contraseñas no son iguales o estan vacias")
            }
        });

        
})

