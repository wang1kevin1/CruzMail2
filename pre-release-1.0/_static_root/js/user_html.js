var myModel = {
    name: "Ashley",
    test: '', 
    test2: '',
    new_mailstop: '',
    new_route: '',
    index: 0,
    allTrue: false,

    new_tracknum: '',
    new_name: '',
    new_sign: '',
    new_email: '',
    new_remark: '',
    Info: [],
    currentView: -1,
    newPackageView: false,
    users: [],
    delete: [],
    
};


var myViewModel = new Vue({
    el: '#my_view',
    delimiters:['${', '}'],
    data: myModel,
    methods: {
	change_to_true: changes_to_true = function(){
	  
	    var allTrue = !myViewModel.allTrue;
	    for(var key in myViewModel.Info){
			myViewModel.Info[key].isDelivered = allTrue;
	    }
	},
	addPackage: addPackages = function(){
	    $.ajax({ type: "POST",
                     url:  '/add_package' ,
                     data:{"track":    myViewModel.new_tracknum,
			   "name":     myViewModel.new_name,
			   "mailstop": myViewModel.new_mailstop,
		           "sign":     myViewModel.new_sign,
		           "email":    myViewModel.new_email,
		           "remark":   myViewModel.new_remark},
                     dataType: 'json',
                     success: function no(response){
                     },
                     error: function(response){
                         console.log("invalid inputs\n");
                     }
            });

	},
	packageDelivered: packagesDelivered = function(){
	   
	 
	    for(var key in myViewModel.Info)
		if(myViewModel.Info[key].isDelivered)
	 	   $.ajax({ type: "POST",
                  	   url:  '/package_delivered' ,
       	                   data:{"pkg_tracking": myViewModel.Info[key].a},
                    	   dataType: 'json',
                           success: function no(response){
                           },
                           error: function(response){
                               console.log("invalid inputs\n");
                           }
                   });

	},
	updatePackage: updatePackages = function(){
	    var objHold = myViewModel.Info[myViewModel.currentView];
		console.log(objHold);
	    $.ajax({ type: "POST",
                     url:  '/update_package' ,
                     data:{
                           "track":  objHold.a,
		     	   "email":  objHold.email,
		     	   "weight": objHold.weight,
		     	   "name":   objHold.name,
		     	   "sign":   objHold.sign},
                     dataType: 'json',
                     success: function no(response){
                     },
                     error: function(response){
                         console.log("invalid inputs\n");
                     }
            });

	},

    user_names: user = function(){
        $.ajax({
            type:"POST",
            url:'/get_users',
            success: function no(response){
                //myViewModel.users = response.user_list;
                //console.log(user_list);
                var objHold;
		         for(var key in response.user_list){
			     
			     objHold = response.user_list[key]
			     myViewModel.users.push({
						    name: objHold.username,
				     		email: objHold.emails,
				     		password: objHold.password,
				     		is_deleted: false,
				     	});
			  
				//console.log(response.params[key]);
			 }      

            },
            error: function(response){

                console.log("No Users\n");
               console.log(user_list);
            }
        });
    },

	delete_user: delete_users = function() {
	  	var self = this;

		var objHold;
		console.log(myViewModel.users.name);
	    for(var key in myViewModel.users){
		if(myViewModel.users[key].is_deleted)
	 	   $.ajax({ 		    
	 	   		url: '/delete_users',
			    type:"POST",
			    data: {"key": myViewModel.users[key].name },
			    dataType: 'json',
                           success: function no(response){
                           	self.users.splice(key,1);

                           },
                           error: function(response){
                               console.log("invalid inputs\n");
                           }
                   });
	 		console.log(myViewModel.users[key]);
	 		}
	 	location.reload();
	},


    user_email: email_list = function(){
        $.ajax({
            type:"POST",
            url:'/get_emails',
            success: function no(response){
                myViewModel.emails = response.user_emails;
                console.log(response.user_emails);
      

            },
            error: function(response){

                console.log("No Users\n");
               //console.log(response.user_emails);
            }
        });
    },


	queryPackage: queryPackages = function(){
	    
	    myViewModel.allTrue = false;
	    myViewModel.currentView = -1;
	    console.log(myViewModel.test);

	    $.ajax({ type: "POST",
		     url:  '/query_package' ,
		     data:{"search": myViewModel.test,
		           "index":  myViewModel.index * 10}, 
		     dataType: 'json',
		     success: function good(response){

			 console.log(response.params);
			 myViewModel.Info = [];
			 var index = 0;
			 var objHold;
		         for(var key in response.params){
			     
			     objHold = response.params[key]
			     myViewModel.Info.push({a: objHold.a,
						    b: objHold.b,
						    c: objHold.c,
						    name: objHold.name,
						    mailstop: objHold.mailstop,
						    sign: objHold.sign,
				     		weight: objHold.weight,
				     		email: objHold.email,
						    isDelivered:false,
						    index: index});
			     index++;
				//console.log(response.params[key]);
			 }
		     },
		     error: function(response){
			 console.log("invalid inputs\n");
		     }
	    });
	}

    }
    
});

myViewModel.user_email();
myViewModel.user_names();
myViewModel.queryPackage();
