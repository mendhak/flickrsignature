
			

			$(document).ready(function() {
		
					$('textarea, input').live('focus mouseup', function(e) {
					if (e.type == 'focusin') {
					this.select();
					}

					if (e.type == 'mouseup') {
					return false;
					}
					});

					$('#generate').click( function() { generateSignature(); } );

					$('#username').keypress(function(event){ keyPressHandler(event); });
					$('#latest').keypress(function(event){ keyPressHandler(event); });
					$('#size').change( function() { generateSignature(); } );
					$('#sort').change( function() { generateSignature(); } );
					$('#linkto').change( function() { generateSignature(); } );
					

			});

			function keyPressHandler(event){
				var keycode = (event.keyCode ? event.keyCode : event.which);
				if(keycode == '13'){
					generateSignature();	
				}
			}

			function generateSignature() { 
				$('#loading').show();
				$('#htmlcode').val('');
				$('#bbcode').val('');
				$('#preview').html('');

				var username = $('#username').val();
				
				if (! $.trim(username) == '') {
					var nsidUrl = 'http://' +  domain + '/nsid/' + $('#username').val();
					$.get(nsidUrl, function(data) {
						generateSignatureFor(data);
					});
				}
				else
				{
					alert('Please fill in a username');
					return;
				}

			}



			function generateSignatureFor(username){

				var latest = $('#latest').val();
				var sortby = $('#sort').val();
				var size = $('#size').val();
				var linkto = $('#linkto').val();
				var overallAnchorStart = '';
				var overallAnchorEnd = '';
				var overallUrlStart = '';
				var overallUrlEnd = '';
				var individualLinks = false;

				switch(linkto){
					case '2':
						overallAnchorStart = '<a href=\"http://www.flickr.com/photos/' + username + '\">';
						overallAnchorEnd = '</a>';
						overallUrlStart = '[url=http://www.flickr.com/photos/' + username + ']';
						overallUrlEnd = '[/url]';
						break;
					case '1':
						individualLinks = true;
						break;
						
				}

				var htmlCode;
				var bbCode;
				htmlCode = overallAnchorStart;	
				bbCode = overallUrlStart;

				for(i = 1; i <= latest; i++){
					if(individualLinks){
						var link = 'http://' + domain + '/url/' + username + '/' + i + '/' + sortby;
						htmlCode += '<a href=\"' + link + '\">';
						bbCode += '[url=' + link + ']';
					}

					var imgSrc = 'http://' + domain + '/img/' + username + '/' + i + '/' + size + '/' + sortby;
					htmlCode += '<img src=\"' + imgSrc + '\" />';
					bbCode += '[img]' + imgSrc + '[/img]';

					if(individualLinks){
						htmlCode += '</a>';
						bbCode += '[/url]';
					}

				}

				htmlCode += overallAnchorEnd;

				//Cleanup, replace //" and //[
				htmlCode = htmlCode.replace(/\/\/"/g, '"');
				htmlCode = htmlCode.replace(/\/"/g, '"');
				bbCode = bbCode.replace(/\/\/\[/g, "[");
				bbCode = bbCode.replace(/\/\[/g, "[");
				bbCode = bbCode.replace(/\/\]/g, "]");

				$('#htmlcode').val(htmlCode);
				$('#bbcode').val(bbCode);
				$('#preview').html(htmlCode);
				$('#loading').hide();
			}
		
