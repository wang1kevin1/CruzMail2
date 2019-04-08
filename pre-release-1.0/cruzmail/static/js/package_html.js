var myModel = {

	//string that stores search string
    search_pkg: '', 

    //true if the general checkbox is checked
    allTrue: false,

    //stores the information for a new package if needed
    new_tracknum: '',
    new_name: '',
    new_sign: '',
    new_email: '',
    new_remark: '',
    new_mailstop: '',
    new_route: '',

    //stores the info for all the packages
    Info: [],

    //checks if extra data wants to be displayed
    // -1: no packages displays extra data
    //positive number: package of the specific index displays extra data
    currentView: -1,

    //checks if the new package overlay is to be displayed
    newPackageView: false,

	users:[],    
};


var myViewModel = new Vue({
    el: '#my_view',
    delimiters:['${', '}'],
    data: myModel,
    methods: {

    //checks all checkbox if the main checkbox is checked
	change_to_true: changes_to_true = function(){
	  
	  	//iterates through every checkbox
	    var allTrue = !myViewModel.allTrue;
	    for(var key in myViewModel.Info){
			myViewModel.Info[key].isDelivered = allTrue;
	    }
	},
	addPackage: addPackages = function(){

		//make ajax with the correct inputs
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
	   
	 
	 	//iterates through packages and checks which packages should be marked
	    for(var key in myViewModel.Info){
	    	//console.log(myViewModel.Info[key].tracking);
			if(myViewModel.Info[key].isDelivered)
		 	   $.ajax({ type: "POST",
	                  	   url:  '/package_delivered' ,
	       	                   data:{"pkg_tracking": myViewModel.Info[key].tracking},
	                    	   dataType: 'json',
	                           success: function no(response){
	                           },
	                           error: function(response){
	                               console.log("invalid inputs\n");
	                           }
	                   });
	    }

	},
	updatePackage: updatePackages = function(){

		//gets the packages that is going to be updated
	    var objHold = myViewModel.Info[myViewModel.currentView];

		//passes right data to be updated
	    $.ajax({ type: "POST",
                     url:  '/update_package' ,
                     data:{
                           "track":  objHold.tracking,
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
	//gets list of packages
	queryPackage: queryPackages = function(){
	    
	    //resets all views
	    myViewModel.allTrue = false;
	    myViewModel.currentView = -1;

	    //gets all the packages with search funtionalities
	    $.ajax({ type: "POST",
		     url:  '/query_package' ,
		     data:{"search": myViewModel.search_pkg,
		           "index":  myViewModel.index * 10}, 
		     dataType: 'json',
		     success: function good(response){

			 console.log(response.params);
			 myViewModel.Info = [];
			 var index = 0;
			 var objHold;

			 	 //gets the data and puts it into an array
			 	 //adds extra variables into each package that are needed
			 	 //isDelivered index 
		         for(var key in response.params){
			     
			     objHold = response.params[key]
			     myViewModel.Info.push({tracking: objHold.pkg_tracking,
										state: objHold.pkg_status,
										date_rec: objHold.pkg_date_rec,
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



    }
    
});

myViewModel.user_email();
myViewModel.user_names();
myViewModel.queryPackage();
