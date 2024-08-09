import React from 'react';
import Sidebar, { SidebarItem } from '../components/Sidebar';
import { LuBarChart3 } from "react-icons/lu";
import { LuLayoutDashboard } from "react-icons/lu";
import { LuUserCircle } from "react-icons/lu";
import { LuReceipt } from "react-icons/lu";
import { LuSettings } from "react-icons/lu";
import { LuHelpCircle } from "react-icons/lu";

const DashBoard = () => {
  return (
    <main className='App'>
      <Sidebar>
        <div className="flex flex-col h-full justify-between">
          <div>
            <SidebarItem icon={<LuLayoutDashboard size={20}/>} text="Dashboard"/>
            <SidebarItem icon={<LuUserCircle size={20}/>} text="Employee" />
            <SidebarItem icon={<LuBarChart3 size={20}/>} text="Attendance" />
            <SidebarItem icon={<LuReceipt size={20}/>} text="Payroll" />
            <hr className='my-3'/>
          </div>
          <div>
            <SidebarItem icon={<LuSettings size={20}/>} text="Settings" />
            <SidebarItem icon={<LuHelpCircle size={20}/>} text="Help" />
          </div>
        </div>
      </Sidebar>
    </main>
  )
}

export default DashBoard;
