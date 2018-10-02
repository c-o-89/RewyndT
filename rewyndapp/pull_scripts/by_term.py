import subprocess
import json
import urllib
import urllib.parse

# twurl must have already been authorized using the "authorize" subcommand

def encode_url(url, qs):
    qs_str = ''
    last = len(qs)
    for i in range(last-1):
        qs_str += qs[i][0]+'='+qs[i][1]+ '"&"'
    qs_str += qs[last-1][0]+'='+qs[last-1][1]
    return url if len(qs_str) == 0 else "{}?{}".format(url, qs_str)


def search(url, qs):
    statuses = []
    counter = 0
    tweetcount = 0
    while True:
        counter += 1
        print(counter)
        full_url = encode_url(url, qs)
        command = "twurl " + full_url
        print(command)
        obj = json.loads(subprocess.check_output(command, shell=True))
        if "statuses" in obj:
            statuses.extend(obj["statuses"])
            search_metadata = obj["search_metadata"]
            tweets = search_metadata.get("count")
            tweetcount += int(tweets)
            next_results = search_metadata.get("next_results")
            if next_results is None:
                print("End of pagination")
                msg = "Parsed {} tweets".format(str(tweetcount))
                print(msg)
                break
            else:
                print("Parsing page")
                qs = urllib.parse.parse_qsl(next_results[1:])
                print(next_results)
                print(qs)
        else:
            print("Statuses not found")
            break
    return statuses


statuses = search('/1.1/search/tweets.json', [
  ('q', '#insecurehbo'),
  ('count', '500'),
  ('result_type', 'recent')
])

out_file = open('output.json', 'a+')
out_file.write(json.dumps(statuses, indent=2))

print("Alright, all done.")

out_file.close()
