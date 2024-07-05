from CID.base.miner import Miner
from CID.base.validator import Validator

class HumanVerificationMiner(Miner):
    def mine(self, data):
        score = 0.00
        score += commit_points(data["total_commits"])
        score += follower_points(data["followers"])
        account_age = time.localtime().tm_year - int(data["created_at"].split('-')[0])
        score += calculate_account_age_points(account_age)
        score += calculate_repo_points(data["public_repos"])
        if data["balance"] > 1:
            score += 0.5
        transactions = data["transaction_count"]
        score += 0.1 * transactions if transactions <= 5 else 0.5
        return score

class HumanVerificationValidator(Validator):
    def validate(self, api_data):
        api_data = json.loads(api_data)
        result = HumanVerificationMiner().mine(api_data)
        score = 0.00
        score += commit_points(api_data["total_commits"])
        score += follower_points(api_data["followers"])
        account_age = time.localtime().tm_year - int(api_data["created_at"].split('-')[0])
        score += calculate_account_age_points(account_age)
        score += calculate_repo_points(api_data["public_repos"])
        if api_data["balance"] > 1:
            score += 0.5
        transactions = api_data["transaction_count"]
        score += 0.1 * transactions if transactions <= 5 else 0.5

        if score == result:
            print("Miner result Verified!")
        else:
            print("Miner result Not Verified!")
        return result
