#!/usr/bin/perl -w
# Syntax- ./gethosts.pl --server VCENTERSERVER -username -password (optional


use strict;
use warnings;
use VMware::VILib;
use VMware::VIRuntime;
 
# validate options, and connect to the server
Opts::parse();
Opts::validate();
Util::connect();
 
 
my $vmhosts = Vim::find_entity_views(view_type => 'HostSystem', properties => ['name']);
open FILE, ">esxhosts";
print "ESX(i) hosts residing on " . Opts::get_option('server') . "\n";
foreach(@$vmhosts) {
        print "\t" . $_->{'name'} . "\n";
        print FILE $_->{'name'} . "\n";
}
close FILE;
Util::disconnect();