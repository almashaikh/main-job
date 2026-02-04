'use client';

import { useState, useEffect } from 'react';
import { 
  Search, 
  MapPin, 
  Calendar, 
  Building, 
  ExternalLink,
  Briefcase,
  Clock,
  Loader2
} from 'lucide-react';

interface Job {
  id: string;
  title: string;
  company: {
    display_name: string;
  };
  location: {
    display_name: string;
  };
  description: string;
  created: string;
  salary_min?: number;
  salary_max?: number;
  redirect_url: string;
  contract_type?: string;
  category: {
    label: string;
  };
}

interface JobSearchResponse {
  results: Job[];
  count: number;
}

export default function JobOpportunitiesPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [location, setLocation] = useState('');
  const [locationSuggestions, setLocationSuggestions] = useState<string[]>([]);
  const [showLocationDropdown, setShowLocationDropdown] = useState(false);
  const [totalJobs, setTotalJobs] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasSearched, setHasSearched] = useState(false);

  // Comprehensive list of Indian locations
  const allLocations = [
    // Major Cities
    'India',
    'Mumbai',
    'Delhi',
    'Bangalore',
    'Hyderabad',
    'Chennai',
    'Kolkata',
    'Pune',
    'Ahmedabad',
    'Jaipur',
    'Surat',
    'Lucknow',
    'Kanpur',
    'Nagpur',
    'Indore',
    'Thane',
    'Bhopal',
    'Visakhapatnam',
    'Pimpri-Chinchwad',
    'Patna',
    'Vadodara',
    'Ghaziabad',
    'Ludhiana',
    'Agra',
    'Nashik',
    'Faridabad',
    'Meerut',
    'Rajkot',
    'Kalyan-Dombivali',
    'Vasai-Virar',
    'Varanasi',
    'Srinagar',
    'Aurangabad',
    'Dhanbad',
    'Amritsar',
    'Navi Mumbai',
    'Allahabad',
    'Ranchi',
    'Howrah',
    'Coimbatore',
    'Jabalpur',
    'Gwalior',
    'Vijayawada',
    'Jodhpur',
    'Madurai',
    'Raipur',
    'Kota',
    'Guwahati',
    'Chandigarh',
    'Solapur',
    'Hubli-Dharwad',
    'Bareilly',
    'Moradabad',
    'Mysore',
    'Gurgaon',
    'Aligarh',
    'Jalandhar',
    'Tiruchirappalli',
    'Bhubaneswar',
    'Salem',
    'Mira-Bhayandar',
    'Warangal',
    'Thiruvananthapuram',
    'Guntur',
    'Bhiwandi',
    'Saharanpur',
    'Gorakhpur',
    'Bikaner',
    'Amravati',
    'Noida',
    'Jamshedpur',
    'Bhilai Nagar',
    'Cuttack',
    'Firozabad',
    'Kochi',
    'Nellore',
    'Bhavnagar',
    'Dehradun',
    'Durgapur',
    'Asansol',
    'Rourkela',
    'Nanded',
    'Kolhapur',
    'Ajmer',
    'Akola',
    'Gulbarga',
    'Jamnagar',
    'Ujjain',
    'Loni',
    'Siliguri',
    'Jhansi',
    'Ulhasnagar',
    'Jammu',
    'Sangli-Miraj & Kupwad',
    'Mangalore',
    'Erode',
    'Belgaum',
    'Ambattur',
    'Tirunelveli',
    'Malegaon',
    'Gaya',
    'Jalgaon',
    'Udaipur',
    'Maheshtala',
    // States
    'Andhra Pradesh',
    'Arunachal Pradesh',
    'Assam',
    'Bihar',
    'Chhattisgarh',
    'Goa',
    'Gujarat',
    'Haryana',
    'Himachal Pradesh',
    'Jharkhand',
    'Karnataka',
    'Kerala',
    'Madhya Pradesh',
    'Maharashtra',
    'Manipur',
    'Meghalaya',
    'Mizoram',
    'Nagaland',
    'Odisha',
    'Punjab',
    'Rajasthan',
    'Sikkim',
    'Tamil Nadu',
    'Telangana',
    'Tripura',
    'Uttar Pradesh',
    'Uttarakhand',
    'West Bengal',
    // Union Territories
    'Andaman and Nicobar Islands',
    'Chandigarh',
    'Dadra and Nagar Haveli and Daman and Diu',
    'Delhi',
    'Jammu and Kashmir',
    'Ladakh',
    'Lakshadweep',
    'Puducherry'
  ];

  const popularRoles = [
    'Software Engineer',
    'Data Scientist', 
    'Python Developer',
    'Full Stack Developer',
    'Frontend Developer',
    'Backend Developer',
    'Machine Learning Engineer',
    'DevOps Engineer'
  ];

  const searchJobs = async (role: string = searchTerm, loc: string = location, page: number = 1) => {
    setLoading(true);
    setHasSearched(true);
    
    try {
      const response = await fetch('http://localhost:8000/api/search-jobs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          role: role,
          location: loc,
          page: page
        }),
      });

      if (response.ok) {
        const data: JobSearchResponse = await response.json();
        
        if (page === 1) {
          setJobs(data.results);
        } else {
          setJobs(prev => [...prev, ...data.results]);
        }
        setTotalJobs(data.count);
        setCurrentPage(page);
      } else {
        console.error('Failed to fetch jobs:', response.status, response.statusText);
      }
    } catch (error) {
      console.error('Error searching jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Load target role from gap analysis if available
    try {
      const savedTargetRole = localStorage.getItem('targetRole')
      if (savedTargetRole && !searchTerm) {
        setSearchTerm(savedTargetRole)
      }
    } catch (e) {
      console.error('Failed to load target role:', e)
    }
  }, []);

  const handleSearch = () => {
    if (!searchTerm.trim()) {
      alert('Please enter a job role to search');
      return;
    }
    
    const searchLocation = location.trim() || 'India'; // Default to India if empty
    setCurrentPage(1);
    searchJobs(searchTerm, searchLocation, 1);
  };

  const handleLocationChange = (value: string) => {
    setLocation(value);
    
    if (value.trim() === '') {
      setLocationSuggestions([]);
      setShowLocationDropdown(false);
      return;
    }

    // Filter locations based on input
    const filtered = allLocations.filter(loc =>
      loc.toLowerCase().includes(value.toLowerCase())
    ).slice(0, 10); // Show max 10 suggestions

    setLocationSuggestions(filtered);
    setShowLocationDropdown(filtered.length > 0);
  };

  const handleLocationSelect = (selectedLocation: string) => {
    setLocation(selectedLocation);
    setShowLocationDropdown(false);
    setLocationSuggestions([]);
  };

  const handleLocationBlur = () => {
    // Delay hiding dropdown to allow click on suggestions
    setTimeout(() => {
      setShowLocationDropdown(false);
    }, 200);
  };

  const handlePopularRoleClick = (role: string) => {
    setSearchTerm(role);
    // Don't automatically search - user must click "Search Jobs" button
  };

  const loadMoreJobs = () => {
    const nextPage = currentPage + 1;
    searchJobs(searchTerm, location, nextPage);
  };

  const formatSalary = (min?: number, max?: number) => {
    if (!min && !max) return null;
    if (min && max) return `₹${min.toLocaleString()} - ₹${max.toLocaleString()}`;
    if (min) return `₹${min.toLocaleString()}+`;
    return `Up to ₹${max?.toLocaleString()}`;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) return '1 day ago';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    return `${Math.floor(diffDays / 30)} months ago`;
  };

  const truncateDescription = (description: string, maxLength: number = 300) => {
    const cleanText = description.replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();
    if (cleanText.length <= maxLength) return cleanText;
    return cleanText.substring(0, maxLength) + '...';
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      {/* Header */}
      <div className="border-b border-gray-800 bg-[#111111] px-6 py-4">
        <h1 className="text-xl font-semibold text-white">Job Opportunities</h1>
        <p className="text-sm text-gray-400 mt-1">Search and discover job opportunities that match your skills</p>
      </div>

      <div className="p-6 space-y-6">
        {/* Search Section */}
        <div className="bg-[#1a1a1a] rounded-lg p-6">
          <h2 className="text-lg font-medium text-white mb-4">Search Jobs</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Job Role</label>
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="e.g. Machine Learning Engineer"
                className="w-full px-4 py-3 bg-[#2a2a2a] border border-gray-700 rounded-md text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              />
            </div>
            
            <div className="relative">
              <label className="block text-sm text-gray-400 mb-2">Location</label>
              <input
                type="text"
                value={location}
                onChange={(e) => handleLocationChange(e.target.value)}
                onFocus={() => {
                  if (location.trim() !== '') {
                    const filtered = allLocations.filter(loc =>
                      loc.toLowerCase().includes(location.toLowerCase())
                    ).slice(0, 10);
                    setLocationSuggestions(filtered);
                    setShowLocationDropdown(filtered.length > 0);
                  }
                }}
                onBlur={handleLocationBlur}
                placeholder="e.g. Mumbai, Delhi, India"
                className="w-full px-4 py-3 bg-[#2a2a2a] border border-gray-700 rounded-md text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              
              {/* Location Dropdown */}
              {showLocationDropdown && locationSuggestions.length > 0 && (
                <div className="absolute z-10 w-full mt-1 bg-[#2a2a2a] border border-gray-700 rounded-md shadow-lg max-h-60 overflow-y-auto">
                  {locationSuggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      type="button"
                      onClick={() => handleLocationSelect(suggestion)}
                      className="w-full px-4 py-2 text-left text-white hover:bg-[#3a3a3a] transition-colors border-b border-gray-700 last:border-b-0"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              )}
            </div>
            
            <div className="flex items-end">
              <button
                type="button"
                onClick={handleSearch}
                disabled={loading}
                className="w-full px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white rounded-md font-medium transition flex items-center justify-center space-x-2"
              >
                <Search className="w-4 h-4" />
                <span>Search Jobs</span>
              </button>
            </div>
          </div>

          {/* Popular Roles */}
          <div>
            <p className="text-sm text-gray-400 mb-3">Popular roles:</p>
            <div className="flex flex-wrap gap-2">
              {popularRoles.map((role) => (
                <button
                  key={role}
                  onClick={() => handlePopularRoleClick(role)}
                  className="px-3 py-2 bg-[#2a2a2a] hover:bg-[#3a3a3a] text-gray-300 text-sm rounded-md transition border border-gray-700"
                >
                  {role}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Job Results */}
        <div className="bg-[#1a1a1a] rounded-lg p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-medium text-white">Job Results</h2>
            {totalJobs > 0 && (
              <span className="text-sm text-gray-400">{jobs.length} jobs found</span>
            )}
          </div>

          {loading && jobs.length === 0 ? (
            <div className="flex items-center justify-center py-16">
              <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
              <span className="ml-3 text-gray-400">Searching for jobs...</span>
            </div>
          ) : !hasSearched ? (
            <div className="text-center py-16">
              <Briefcase className="w-16 h-16 text-gray-600 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-white mb-2">Ready to find your next opportunity?</h3>
              <p className="text-gray-400">Enter a job role and location above, then click "Search Jobs" to get started.</p>
            </div>
          ) : jobs.length === 0 ? (
            <div className="text-center py-16">
              <Briefcase className="w-16 h-16 text-gray-600 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-white mb-2">No jobs found</h3>
              <p className="text-gray-400">Try adjusting your search criteria or search for a different role.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {jobs.map((job, index) => (
                <div key={`${job.id}-${index}`} className="bg-[#2a2a2a] rounded-lg p-6 border border-gray-700 hover:border-gray-600 transition">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-white mb-2 hover:text-blue-400 cursor-pointer">
                        {job.title}
                      </h3>
                      <div className="flex items-center space-x-6 text-sm text-gray-400 mb-3">
                        <div className="flex items-center space-x-2">
                          <Building className="w-4 h-4" />
                          <span>{job.company.display_name || 'Company Not Specified'}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <MapPin className="w-4 h-4" />
                          <span>{job.location.display_name}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Calendar className="w-4 h-4" />
                          <span>{formatDate(job.created)}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="text-right flex flex-col items-end space-y-2">
                      <a
                        href={job.redirect_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-md transition flex items-center space-x-2 no-underline"
                        onClick={(e) => {
                          // Ensure the link works properly
                          if (!job.redirect_url || job.redirect_url === '#') {
                            e.preventDefault();
                            alert('Job application link not available');
                          }
                        }}
                      >
                        <span>Apply</span>
                        <ExternalLink className="w-4 h-4" />
                      </a>
                      {job.category?.label && (
                        <span className="px-2 py-1 bg-blue-600/20 text-blue-400 text-xs rounded">
                          IT Jobs
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="mb-4">
                    {formatSalary(job.salary_min, job.salary_max) ? (
                      <div className="flex items-center space-x-2 text-green-400 text-sm mb-2">
                        <span>{formatSalary(job.salary_min, job.salary_max)}</span>
                      </div>
                    ) : (
                      <div className="flex items-center space-x-2 text-green-400 text-sm mb-2">
                        <span>Salary not specified</span>
                      </div>
                    )}
                  </div>

                  <p className="text-gray-300 text-sm leading-relaxed mb-4">
                    {truncateDescription(job.description)}
                  </p>

                  <div className="flex items-center justify-between text-xs text-gray-500">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-1">
                        <Clock className="w-3 h-3" />
                        <span>{job.contract_type || 'Full Time'}</span>
                      </div>
                    </div>
                    
                    <a
                      href={job.redirect_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-400 hover:text-blue-300 transition no-underline"
                      onClick={(e) => {
                        if (!job.redirect_url || job.redirect_url === '#') {
                          e.preventDefault();
                          alert('Job application link not available');
                        }
                      }}
                    >
                      View Details →
                    </a>
                  </div>
                </div>
              ))}

              {/* Load More Button */}
              {jobs.length > 0 && jobs.length < totalJobs && (
                <div className="text-center pt-6">
                  <button
                    onClick={loadMoreJobs}
                    disabled={loading}
                    className="px-8 py-3 bg-[#2a2a2a] hover:bg-[#3a3a3a] disabled:bg-[#2a2a2a] text-white rounded-md transition flex items-center space-x-2 mx-auto border border-gray-700"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        <span>Loading...</span>
                      </>
                    ) : (
                      <span>Load More Jobs</span>
                    )}
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}