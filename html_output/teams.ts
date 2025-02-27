import { FaTwitter, FaLinkedin } from "react-icons/fa";
 
const teams = [
  {
    teamName: "Team Alpha",
    teamDescription: "This is Team Alpha's description.",
    members: [
      {
        imageSrc: "/images/team/alpha/member1.jpg",
        name: "Member One",
        description: "Description for member one.",
        socialLinks: [
          { icon: FaTwitter, url: "https://twitter.com/member1" },
          { icon: FaLinkedin, url: "https://linkedin.com/in/member1" }
        ]
      },
      {
        imageSrc: "/images/team/alpha/member2.jpg",
        name: "Member Two",
        description: "Description for member two.",
        socialLinks: [
          { icon: FaTwitter, url: "https://twitter.com/member2" },
          { icon: FaLinkedin, url: "https://linkedin.com/in/member2" }
        ]
      },
      {
        imageSrc: "/images/team/alpha/member1.jpg",
        name: "Member four",
        description: "Description for member one.",
        socialLinks: [
          { icon: FaTwitter, url: "https://twitter.com/member1" },
          { icon: FaLinkedin, url: "https://linkedin.com/in/member1" }
        ]
      },
      {
        imageSrc: "/images/team/alpha/member1.jpg",
        name: "Member three",
        description: "Description for member one.",
        socialLinks: [
          { icon: FaTwitter, url: "https://twitter.com/member1" },
          { icon: FaLinkedin, url: "https://linkedin.com/in/member1" }
        ]
      },
      {
        imageSrc: "/images/team/alpha/member1.jpg",
        name: "Member five",
        description: "Description for member one.",
        socialLinks: [
          { icon: FaTwitter, url: "https://twitter.com/member1" },
          { icon: FaLinkedin, url: "https://linkedin.com/in/member1" }
        ]
      }
    ]
  },
  {
    teamName: "Team Beta",
    teamDescription: "This is Team Beta's description.",
    members: [
      {
        imageSrc: "/images/team/beta/member1.jpg",
        name: "Member Three",
        description: "Description for member three.",
        socialLinks: [
          { icon: FaTwitter, url: "https://twitter.com/member3" },
          { icon: FaLinkedin, url: "https://linkedin.com/in/member3" }
        ]
      }
    ]
  }
];
 
export default teams;