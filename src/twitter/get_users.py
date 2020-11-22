"""
Script to get @mentions to bot in given time window
"""

import yaml


def main():

    users = get_users()
    write_users(users)

    seed_parameters = read_seed_parameters()
    update_seed_parameters(seed_parameters, len(users))


def get_users():
    """Mock getting users from Twitter API"""

    with open("./mock_users.yml", "r") as f:
        users = yaml.load(f, Loader=yaml.FullLoader)
    return users


def write_users(users):
    """Write users to temporary file"""

    with open("../../output/users.tmp", "w") as f:
        yaml.dump(users, f)


def read_seed_parameters():
    """Read seed parameters from temporary file"""

    with open("../../output/seed.tmp", "r") as f:
        seed = int(f.readline())
        samples = int(f.readline())
    return (seed, samples)


def update_seed_parameters(parameters, samples):
    """Update seed file with new starting seed and number of samples to be generated"""

    with open("../../output/seed.tmp", "w") as f:
        f.write(f"{parameters[0]+parameters[1]}\n")
        f.write(f"{samples}")


if __name__ == "__main__":
    main()