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
    
    new_weight: null,
    new_height: null,
    new_width:  null,
    new_length: null,

    new_route: '',

    //stores the information of advanced search
    adv_mailstop: '',
    adv_name: '',
    adv_status: 'not delivered',
    adv_email: '',
    adv_signing: '',

    //stores the info for all the packages
    Info: [],
    auto_fill: [],

    //checks if extra data wants to be displayed
    // -1: no packages displays extra data
    //positive number: package of the specific index displays extra data
    currentView: -1,

    //checks if the new package overlay is to be displayed
    newPackageView: false,
    advancedSearchView: false,

    no_result_for_autofill: false,

	//checks if the new package overlay is to be displayed
	newPackageView: false,
	
	//checks if the import overlay is to be displayed
	newImportView: false,

	//keeps track of whether the user has tried searching yet
	customer_search: false,
	customer_status: null,
	customer_track_num: null,
	customer_dest: null,
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
		           		   "remark":   myViewModel.new_remark,
		           		   "weight":   myViewModel.new_weight,
		           		   "width":    myViewModel.new_width,
		           		   "height":   myViewModel.new_height,
		           		   "length":   myViewModel.new_length},
                     dataType: 'json',
                     success: function no(response){
                     	location.reload();
                     },
                     error: function(response){
                         console.log("invalid inputs\n");
                     }
            });

	},
	packageDelivered: packagesDelivered = function(){
	   
	 
	 	//iterates through packages and checks which packages should be marked
	    for(var key in myViewModel.Info){
	    	//console.log(myViewModel.Info[key].state);
			if(myViewModel.Info[key].isDelivered && myViewModel.Info[key].state == "received")
				//console.log("a");
		 	   $.ajax({ type: "POST",
	                  	   url:  '/package_delivered' ,
	       	                   data:{"pkg_tracking": myViewModel.Info[key].tracking,
	       	               			 "pkg_email": myViewModel.Info[key].email,
	       	               			 "mailstop": myViewModel.Info[key].mailstop},
	                    	   dataType: 'json',
	                           success: function no(response){
	                           		location.reload();
	                           },
	                           error: function(response){
	                               console.log("invalid inputs\n");
	                           }
	                   });
	    }
	    //myViewModel.queryPackage();

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
				     	   "sign":   objHold.sign,
				     	   "width":  objHold.pkg_width,
				     	   "height": objHold.pkg_height,
				     	   "length": objHold.pkg_length},
                     dataType: 'json',
                     success: function no(response){
                     	location.reload();
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

	    //resets customer's previous query
	    myViewModel.customer_status = null;
		myViewModel.customer_track_num = null;
		myViewModel.customer_dest = null;

	    //gets all the packages with search funtionalities
	    $.ajax({ type: "POST",
		     url:  '/query_package' ,
		     data:{"search":   myViewModel.search_pkg,
		           "index":    myViewModel.index * 10,
		       	   "mailstop": myViewModel.adv_mailstop,
		       	   "name":     myViewModel.adv_name,
		       	   "email":    myViewModel.adv_email,
		       	   "status":   myViewModel.adv_status,
		       	   "signing":  myViewModel.adv_signing }, 
		     dataType: 'json',
		     success: function good(response){

		     //user has searched
		     myViewModel.customer_search = true;

			 myViewModel.Info = [];

			 //variable for keeping track of when an item is added
			 var index = 0;
			 var objHold;

			 	 //gets the data and puts it into an array
			 	 //adds extra variables into each package that are needed
			 	 //isDelivered index 
		         for(var key in response.params){
					     objHold = response.params[key]
					     myViewModel.Info.push({tracking:     objHold.pkg_tracking,
												state:        objHold.pkg_status,
												date_rec:     objHold.pkg_date_rec,
								    			name:         objHold.name,
								    			mailstop:     objHold.mailstop,
								    			sign:         objHold.sign,
						     					weight:       objHold.weight,
						     					email:        objHold.email,
						     					pkg_width:    objHold.pkg_width,
						     					pkg_height:   objHold.pkg_height,
						     					pkg_length:   objHold.pkg_length,
						     					pkg_remarks:  objHold.pkg_remarks,

								    			isDelivered:false,
								    			index: index});
					     index++;
					 if(myViewModel.search_pkg == objHold.pkg_tracking){
					 	myViewModel.customer_status = objHold.pkg_status;
						myViewModel.customer_track_num = objHold.pkg_tracking;
						myViewModel.customer_dest = objHold.mailstop;

					 }
					 
				//console.log(response.params[key]);
			 }

		     },
		     error: function(response){
			 console.log("invalid inputs\n");
			 customer_search = true;
		     }
	    });
	},

	queryPerson: queryPeople = function () {

		myViewModel.no_result_for_autofill = false;
		if(myViewModel.new_name != "" && myViewModel != null)
	      	$.ajax({
	        	type: "POST",
	        	url: '/query_person',
	        	data: {
	        	  "search": myViewModel.new_name,
	        	  "index": 10
	       	 },
	       	 dataType: 'json',
	       	 success: function good(response) {

	       	 	  //check if result is found
	       	 	  if(response.params.length == 0){
	       	 	  	 myViewModel.no_result_for_autofill = true;
	       	 	  }
	        	  myViewModel.auto_fill = [];
	        	  var index = 0;
	       	  	  var objHold;
	        	  for (var key in response.params) {

	        	  	  var objHold = response.params[key]
	           		  myViewModel.auto_fill.push({
	              	  	  name: objHold.name,
	              	  	  ppl_email: objHold.ppl_email,
	                  	  mailstop: objHold.mailstop,
	            	  });

	                  console.log(response.params[key]);
	          	  }
	        },
	        error: function (response) {
	          console.log("invalid inputs\n");
	        }
	      });
    },
    autoFill_name: autofill_names = function (new_auto_name, new_auto_mailstop, new_auto_email) {
    	myViewModel.auto_fill = [];
    	myViewModel.new_name = new_auto_name;
    	myViewModel.new_mailstop = new_auto_mailstop;
    	myViewModel.new_email = new_auto_email;
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
