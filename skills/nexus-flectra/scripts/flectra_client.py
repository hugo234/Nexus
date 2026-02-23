import os
import sys
import argparse
import xmlrpc.client
import json

def get_credentials():
    url = os.environ.get('FLECTRA_URL')
    db = os.environ.get('FLECTRA_DB')
    user = os.environ.get('FLECTRA_USER')
    password = os.environ.get('FLECTRA_PASSWORD')
    
    if not all([url, db, user, password]):
        print("Error: Missing Flectra/Odoo credentials. Please set FLECTRA_URL, FLECTRA_DB, FLECTRA_USER, and FLECTRA_PASSWORD environment variables.", file=sys.stderr)
        sys.exit(1)
        
    return url, db, user, password

def get_uid(url, db, user, password):
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, user, password, {})
    if not uid:
        print("Error: Authentication failed.", file=sys.stderr)
        sys.exit(1)
    return uid

def execute_kw(url, db, uid, password, model, method, *args, **kwargs):
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    return models.execute_kw(db, uid, password, model, method, args, kwargs)

def main():
    parser = argparse.ArgumentParser(description='Nexus Flectra/Odoo XML-RPC Client.')
    parser.add_argument('--action', required=True, choices=['search_read', 'search', 'read', 'create', 'write', 'unlink'], help='The action to perform.')
    parser.add_argument('--model', required=True, help='The Flectra model (e.g., res.partner).')
    parser.add_argument('--domain', type=str, default='[]', help='Domain for search actions (JSON format).')
    parser.add_argument('--fields', type=str, default='[]', help='Fields to read (JSON format).')
    parser.add_argument('--limit', type=int, default=10, help='Limit results.')
    
    args = parser.parse_args()
    
    url, db, user, password = get_credentials()
    uid = get_uid(url, db, user, password)
    
    try:
        domain = json.loads(args.domain)
        fields = json.loads(args.fields)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON args: {e}", file=sys.stderr)
        sys.exit(1)
        
    try:
        if args.action == 'search_read':
            result = execute_kw(url, db, uid, password, args.model, 'search_read', [domain], {'fields': fields, 'limit': args.limit})
        elif args.action == 'search':
            result = execute_kw(url, db, uid, password, args.model, 'search', [domain], {'limit': args.limit})
        elif args.action == 'read':
            result = execute_kw(url, db, uid, password, args.model, 'read', domain, {'fields': fields})
        else:
            print(f"Action {args.action} is not fully implemented in this template yet.", file=sys.stderr)
            sys.exit(1)
            
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"XML-RPC Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
