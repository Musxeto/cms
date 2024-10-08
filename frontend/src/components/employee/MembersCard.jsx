import React from "react";

const MembersCard = ({ profileImage, name, department, position, username, email, phone }) => {
  return (
    <div className="flex items-center bg-white hover:bg-gray-200 transition-all rounded-lg shadow-md p-4 mb-4 w-full">
      {/* Profile Image */}
      <div className="w-24 h-24 overflow-hidden rounded-full mr-4">
        <img
          src={profileImage}
          alt={`${name}'s profile`}
          className="w-full h-full object-cover"
        />
      </div>

      {/* Member Info */}
      <div className="flex-grow">
        <h3 className="text-xl font-semibold">{name}</h3>
        <p className="text-gray-600">{position}</p>
        <p className="text-gray-600">{department}</p>
        {username && <p className="text-sm text-gray-500">@{username}</p>}
        {email && <p className="text-sm text-gray-500">{email}</p>}
        {phone && <p className="text-sm text-gray-500">{phone}</p>}
      </div>
    </div>
  );
};

export default MembersCard;
