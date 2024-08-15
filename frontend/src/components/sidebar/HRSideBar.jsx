import React from "react";
import Sidebar, { SidebarItem } from "./Sidebar";
import {
  FaHome,
  FaUsers,
  FaCalendarAlt,
  FaUser,
  FaDollarSign,
  FaStar,
  FaPaperPlane,
  FaBriefcase,
  FaUserPlus,
  FaBuilding,
  FaRocket,
} from "react-icons/fa";
import { Settings, LogOut } from "lucide-react";
import { useAuth } from "../../contexts/AuthContext";

const HRSideBar = () => {
  const { logout } = useAuth();

  return (
    <Sidebar>
      <SidebarItem icon={<FaHome />} text="Dashboard" to="/hr/dashboard" />
      <SidebarItem
        icon={<FaBriefcase />}
        text="Job Postings"
        to="/hr/job-postings"
      />
      <SidebarItem
        icon={<FaPaperPlane />}
        text="Job Applications"
        to="/hr/applications"
      />
      <SidebarItem
        icon={<FaRocket />}
        text="Talent Hunt"
        to="/hr/talent-hunt"
      />
      <SidebarItem
        icon={<FaCalendarAlt />}
        text="Attendance"
        to="/hr/attendance"
      />
      <SidebarItem icon={<FaDollarSign />} text="Payroll" to="/hr/payroll" />
      <SidebarItem
        icon={<FaUsers />}
        text="Employees List"
        to="/hr/employees"
      />
      <SidebarItem
        icon={<FaBuilding />}
        text="Employees List"
        to="/hr/departments"
      />
      <SidebarItem icon={<FaUser />} text="Profile" to="/hr/profile" />
      <hr className="my-3" />
      <SidebarItem icon={<Settings />} text="Settings" to="/hr/settings" />
      <SidebarItem icon={<LogOut />} text="Logout" onClick={logout} />
      
    </Sidebar>
  );
};

export default HRSideBar;
