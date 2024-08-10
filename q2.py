class SocialGraph:
    def __init__(self):
        self.friends = {}
    
    def add_friendship(self, person, friend):
        if person not in self.friends:
            self.friends[person] = set()
        if friend not in self.friends:
            self.friends[friend] = set()
        self.friends[person].add(friend)
        self.friends[friend].add(person)
    
    def common_friends(self, person1, person2):
        return list(self.friends[person1].intersection(self.friends[person2]))
    
    def find_connection_level(self, start, end):
        if start not in self.friends or end not in self.friends:
            return -1
        if start == end:
            return 0
        queue = [(start, 0)]
        visited = set([start])
        while queue:
            current, level = queue.pop(0)
            for friend in self.friends[current]:
                if friend == end:
                    return level + 1
                if friend not in visited:
                    visited.add(friend)
                    queue.append((friend, level + 1))
        return -1

def main():
    graph = SocialGraph()
    # Example additions - this part would ideally read input or a file
    graph.add_friendship("Alice", "Bob")
    graph.add_friendship("Bob", "Janice")
    graph.add_friendship("Alice", "Clara")
    graph.add_friendship("Clara", "Bob")
    
    # Example usage - replace with console input handling
    print("Common friends of Alice and Bob:", graph.common_friends("Alice", "Bob"))
    print("Connection level from Alice to Janice:", graph.find_connection_level("Alice", "Janice"))

if __name__ == "__main__":
    main()