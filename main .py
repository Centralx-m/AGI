"""
Main Entry Point - Unlimited Autonomous AI Agent
=================================================

This is the main script to run the Unlimited Autonomous AI Agent.
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.unlimited_agent import UnlimitedAgent
from src.core.memory import CoreMemory
from src.tasks.task_manager import TaskManager


def create_demo_tasks(agent: UnlimitedAgent) -> TaskManager:
    """
    Create demo tasks to test the agent
    
    Args:
        agent: The agent to add tasks to
    
    Returns:
        TaskManager: The task manager with tasks
    """
    task_manager = TaskManager(agent)
    
    # Add a trading task
    task_manager.add_task(
        description="Analyze the current cryptocurrency market and identify trading opportunities",
        priority=5,
        context={'market': 'crypto', 'timeframe': '1h'},
        deadline="2024-12-31"
    )
    
    # Add a business task
    task_manager.add_task(
        description="Create a business plan for a new AI startup",
        priority=4,
        context={'industry': 'AI', 'phase': 'seed'},
        deadline="2024-12-15"
    )
    
    # Add a bot creation task
    task_manager.add_task(
        description="Create a new bot that can analyze customer sentiment from social media",
        priority=3,
        context={'platform': 'twitter', 'language': 'all'},
        deadline="2025-01-15"
    )
    
    # Add a learning task
    task_manager.add_task(
        description="Learn about quantum computing and its business applications",
        priority=2,
        context={'field': 'quantum', 'level': 'intermediate'},
        deadline="2025-02-01"
    )
    
    print(f"📋 Added {len(task_manager.tasks)} demo tasks")
    
    return task_manager


def main():
    """
    Main entry point
    """
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🤖 UNLIMITED AUTONOMOUS AI AGENT                                          ║
║                                                                              ║
║   "The AI that can do ANY task, in ANY domain, ANYWHERE"                    ║
║                                                                              ║
║   Features:                                                                  ║
║   - Self-learning from books and experience                                ║
║   - Self-repairing when something breaks                                   ║
║   - Self-upgrading to become better                                         ║
║   - Self-replicating to create other bots                                  ║
║                                                                              ║
║   Domains: Business, Finance, Healthcare, Education, Technology, Legal,     ║
║             Creative, Real Estate, Manufacturing, Agriculture, Retail,       ║
║             Transportation, Energy, Government, and more...                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Initialize the agent
    print("\n" + "="*70)
    print("INITIALIZING AGENT...")
    print("="*70)
    
    agent = UnlimitedAgent()
    
    # Step 2: Add demo tasks
    print("\n" + "="*70)
    print("ADDING TASKS...")
    print("="*70)
    
    task_manager = create_demo_tasks(agent)
    
    # Step 3: Show initial status
    print("\n" + "="*70)
    print("INITIAL STATUS")
    print("="*70)
    
    status = agent.get_status()
    print(json.dumps(status, indent=2, default=str))
    
    # Step 4: Ask user what to do
    print("\n" + "="*70)
    print("WHAT WOULD YOU LIKE TO DO?")
    print("="*70)
    print("1. Process all pending tasks")
    print("2. Process one specific task")
    print("3. Add a new task")
    print("4. Create a new bot")
    print("5. Run autonomously")
    print("6. Show status")
    print("7. Exit")
    
    # Get user choice
    choice = input("\nEnter your choice (1-7): ").strip()
    
    if choice == "1":
        # Process all tasks
        print("\n🔄 Processing all tasks...")
        pending = task_manager.get_pending_tasks()
        for task in pending:
            result = agent.process_task(task['description'], task.get('context'))
            task_manager.mark_completed(task['id'], result)
            print(f"✅ Task {task['id']} completed: {result['success']}")
    
    elif choice == "2":
        # Process one specific task
        task_id = input("Enter task ID: ").strip()
        task = task_manager.get_task_by_id(task_id)
        if task:
            result = agent.process_task(task['description'], task.get('context'))
            task_manager.mark_completed(task['id'], result)
            print(f"✅ Task completed: {result['success']}")
        else:
            print(f"❌ Task {task_id} not found")
    
    elif choice == "3":
        # Add a new task
        description = input("Enter task description: ").strip()
        context_input = input("Enter context (JSON format, or press Enter for empty): ").strip()
        context = json.loads(context_input) if context_input else {}
        priority = int(input("Enter priority (1-5): ").strip() or "3")
        
        task_id = task_manager.add_task(description, priority, context)
        print(f"✅ Task added with ID: {task_id}")
    
    elif choice == "4":
        # Create a new bot
        requirements = input("Enter bot requirements: ").strip()
        location = input("Enter location (local/cloud/remote): ").strip() or "local"
        
        # Use the bot creator
        from src.core.unlimited_agent import Task_CreateBot
        creator = Task_CreateBot(agent)
        result = creator.execute(requirements, location)
        
        if result['success']:
            print(f"✅ Bot created at: {result['location']}")
        else:
            print(f"❌ Bot creation failed")
    
    elif choice == "5":
        # Run autonomously
        print("\n🤖 Starting autonomous mode...")
        print("   The agent will process tasks automatically")
        print("   Press Ctrl+C to stop")
        agent.run_autonomously()
    
    elif choice == "6":
        # Show status
        status = agent.get_status()
        print(json.dumps(status, indent=2, default=str))
    
    else:
        print("👋 Goodbye!")
    
    # Step 5: Show final status
    print("\n" + "="*70)
    print("FINAL STATUS")
    print("="*70)
    
    status = agent.get_status()
    print(json.dumps(status, indent=2, default=str))
    
    print("\n✅ Agent execution complete!")


if __name__ == "__main__":
    main()