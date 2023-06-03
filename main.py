from scanner import Scanner

if __name__.__eq__('__main__'):
    scan = Scanner()
    scan.set_consulate_code(93104)
    scan.set_application_number(11571)
    scan.set_application_date('20230313')
    scan.set_scanning_depth(applications=571)
    scan.start_scanning()
