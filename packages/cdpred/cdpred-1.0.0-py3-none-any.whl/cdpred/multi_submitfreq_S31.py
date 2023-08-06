
import csv, sys

ran = str(sys.argv[1])
serv = "cdpred_"
dir = serv+ran
#print(dir)

csvFile = open('/usr1/webserver/cgidocs/tmp/cdpred/'+dir+'/Out777')#enter the csv filename
#csvReader = csv.reader(csvFile,delimiter='\t')
#csvData = list(csvReader)


with open('/usr1/webserver/cgidocs/tmp/cdpred/'+dir+'/output.html'+ran, 'w') as html: #enter the output filename
    html.write('''<!-- Latest compiled and minified CSS -->
                <link rel="stylesheet" href="assets/css/bootstrap-table.min.css" />
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
''')    
    html.write('<table data-toggle = "table" data-pagination = "true">\r')

    with open('/usr1/webserver/cgidocs/tmp/cdpred/'+dir+'/Out777') as file:
     r = 0
     for row in file.read().split('\n')[:-1]:
        if r == 0:
            html.write('\t<thead style="font-weight:bold;">\r\t\t<tr>\r')
            for col in row.split('\t'):
                html.write('\t\t\t<th data-sortable="true">' + col + '</th>\r')
            html.write('\t\t</tr>\r\t</thead>\r')
            html.write('\t<tbody>\r')
        else:
            html.write('\t\t<tr>\r')
            for col in row.split('\t'):
                html.write('\t\t\t<td>' + col + '</td>\r')
            html.write('\t\t</tr>\r')

        r += 1
    html.write('\t</tbody>\r')
    html.write('</table>\r')
    
    html.write('''
<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.0/jquery.min.js"></script>

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

<!-- Latest compiled and minified JavaScript -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.8.1/bootstrap-table.min.js"></script>
''')




#with open('/usr1/webserver/cgidocs/tmp/il4pred/'+dir+'/output.html') as display:
#    for line in display.read().split('\n'):
#            print line 

